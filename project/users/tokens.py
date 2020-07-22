from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self,user,timestamp):
        return ( six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active) )


account_activation_token = TokenGenerator()


class EmailTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.profile.email_confirmed)
        )

email_confirmation_token = EmailTokenGenerator()


class ChangeEmailTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self,user,timestamp):
        return ( six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.is_active) + six.text_type(user.email)
        )


change_email_token = ChangeEmailTokenGenerator()


