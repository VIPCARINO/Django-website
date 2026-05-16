from allauth.socialaccount.signals import social_account_added
from django.dispatch import receiver

@receiver(social_account_added)
def save_google_email(request, sociallogin, **kwargs):
    user = sociallogin.user

    extra_data = sociallogin.account.extra_data

    if not user.email and "email" in extra_data:
        user.email = extra_data["email"]
        user.save()