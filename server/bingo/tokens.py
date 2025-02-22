from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        email_field = user.get_email_field_name()
        email = getattr(user, email_field)
        return f"{user.pk}{timestamp}{email}"


email_verification_token_generator = EmailVerificationTokenGenerator()
