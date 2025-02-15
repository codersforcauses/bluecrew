from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import User
from ..tokens import email_verification_token_generator
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.password_validation import validate_password
from django.urls import reverse
from smtplib import SMTPException, SMTPSenderRefused


@api_view(['POST'])
def request_email_verification(request):
    try:
        email = request.POST['email']
        user = User.objects.get(email=email)
    except (ObjectDoesNotExist, KeyError):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if user.is_active:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    encoded_user = urlsafe_base64_encode(force_bytes(user.pk))
    token = email_verification_token_generator.make_token(user)
    url = request.build_absolute_uri(f"{reverse("confirm_email")}?uid64={encoded_user}&token={token}")
    content = render_to_string(
        "verification.html",
        context={"url": url}
    )
    message = EmailMessage(
        "Bingo Email Verification",
        content,
        settings.ACCOUNTS_EMAIL,
        list(email)
    )
    message.content_subtype = "html"
    try:
        message.send(fail_silently=False)
    except SMTPSenderRefused:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except SMTPException:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
def confirm_email(request):
    success_path = settings.FRONTEND_URL

    try:
        uid64 = request.GET["uid64"]
        token = request.GET["token"]
        uid = force_str(urlsafe_base64_decode(uid64))
    except (KeyError, ValueError):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    user = get_object_or_404(User, user_id=uid)
    if user.is_active:
        return redirect(success_path)
    if not email_verification_token_generator.check_token(user, token):
        return Response(status=status.HTTP_404_NOT_FOUND)
    user.is_active = True
    user.save()
    return redirect(success_path)


@api_view(["POST"])
def request_password_reset(request):
    try:
        email = request.POST['email']
        user = User.objects.get(email=email)
    except (ObjectDoesNotExist, KeyError):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    token = default_token_generator.make_token(user)
    encoded_user = urlsafe_base64_encode(force_bytes(user.pk))
    # TODO Replace with link to the actual reset form
    url = request.build_absolute_uri(f"{settings.FRONTEND_URL}/{"reset_path"}/?uid64={encoded_user}&token={token}")
    content = render_to_string(
        "password_reset.html",
        context={"url": url}
    )
    message = EmailMessage(
        "Bingo Password Reset",
        content,
        settings.ACCOUNTS_EMAIL,
        list(email)
    )
    message.content_subtype = "html"
    try:
        message.send(fail_silently=False)
    except SMTPSenderRefused:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except SMTPException:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
def reset_password(request):
    try:
        uid64 = request.data["uid"]
        token = request.data["token"]
        password = request.data["password"]
        uid = force_str(urlsafe_base64_decode(uid64))
    except (KeyError, ValueError):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        validate_password(password)
    except ValidationError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    user = get_object_or_404(User, user_id=uid)
    if not default_token_generator.check_token(user, token):
        return Response(status=status.HTTP_404_NOT_FOUND)

    user.set_password(password)
    user.save()
    return Response(status=status.HTTP_200_OK)
