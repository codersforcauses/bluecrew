from django.shortcuts import get_object_or_404
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
from smtplib import SMTPException, SMTPRecipientsRefused
from django.utils.safestring import mark_safe


@api_view(['POST'])
def request_email_verification(request):
    try:
        email = request.data['email']
        user = User.objects.get(email=email)
    except ObjectDoesNotExist:
        return Response("No user with this email.", status=status.HTTP_400_BAD_REQUEST)
    except KeyError:
        return Response("No email provided.", status=status.HTTP_400_BAD_REQUEST)

    if user.is_active:
        return Response("User already has verified email.", status=status.HTTP_400_BAD_REQUEST)
    encoded_user = urlsafe_base64_encode(force_bytes(user.pk))
    token = email_verification_token_generator.make_token(user)
    url = mark_safe(
        f"{settings.FRONTEND_URL}/verify-email?uid64={encoded_user}&token={token}")
    content = render_to_string(
        "verification.html",
        context={"url": url}
    )
    message = EmailMessage(
        "Bingo Email Verification",
        content,
        settings.ACCOUNTS_EMAIL,
        [email]
    )
    message.content_subtype = "html"
    try:
        message.send(fail_silently=False)
    except SMTPRecipientsRefused:
        return Response("Provided address refused to accept email.", status=status.HTTP_400_BAD_REQUEST)
    except SMTPException:
        return Response("The email backend failed.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
def confirm_email(request):
    try:
        uid64 = request.data["uid64"]
        token = request.data["token"]
        uid = force_str(urlsafe_base64_decode(uid64))
    except (KeyError, ValueError):
        return Response("User ID or token was missing or invalid", status=status.HTTP_400_BAD_REQUEST)

    user = get_object_or_404(User, user_id=uid)
    if user.is_active:
        return Response("User already has verified email.", status=status.HTTP_200_OK)
    if not email_verification_token_generator.check_token(user, token):
        return Response("Token invalid", status=status.HTTP_404_NOT_FOUND)
    user.is_active = True
    user.save()
    return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
def request_password_reset(request):
    try:
        email = request.data['email']
        user = User.objects.get(email=email)
    except ObjectDoesNotExist:
        return Response("No user with this email.", status=status.HTTP_400_BAD_REQUEST)
    except KeyError:
        return Response("No email provided.", status=status.HTTP_400_BAD_REQUEST)

    token = default_token_generator.make_token(user)
    encoded_user = urlsafe_base64_encode(force_bytes(user.pk))
    url = mark_safe(
        f"{settings.FRONTEND_URL}/forgot-password/?uid64={encoded_user}&token={token}")
    content = render_to_string(
        "password_reset.html",
        context={"url": url, "username": user.username,
                 "name": user.first_name}
    )
    message = EmailMessage(
        "Bingo Password Reset",
        content,
        settings.ACCOUNTS_EMAIL,
        [email]
    )
    message.content_subtype = "html"
    try:
        message.send(fail_silently=False)
    except SMTPRecipientsRefused:
        return Response("Provided address refused to accept email.", status=status.HTTP_400_BAD_REQUEST)
    except SMTPException:
        return Response("The email backend failed.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
def reset_password(request):
    try:
        uid64 = request.data["uid64"]
        token = request.data["token"]
        password = request.data["password"]
        uid = force_str(urlsafe_base64_decode(uid64))
        validate_password(password)
    except KeyError:
        return Response("User ID, token, or password missing.", status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response("User ID invalid.", status=status.HTTP_400_BAD_REQUEST)
    except ValidationError as password_errors:
        return Response(password_errors, status=status.HTTP_400_BAD_REQUEST)

    user = get_object_or_404(User, user_id=uid)
    if not default_token_generator.check_token(user, token):
        return Response("Token invalid", status=status.HTTP_404_NOT_FOUND)

    user.set_password(password)
    user.save()
    return Response(status=status.HTTP_200_OK)
