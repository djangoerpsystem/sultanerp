from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import LoginLog


# https://docs.djangoproject.com/en/4.2/ref/contrib/auth/
# "https: // docs.djangoproject.com/en/4.2/topics/signals/"
# basically for logging the user log ins and log outs
@receiver(user_logged_in)
def user_logged_in_receiver(sender, request, user, **kwargs):
    print("Signal triggered")
    LoginLog.objects.create(user=user, loggedIn=True)

@receiver(user_logged_out)
def user_logged_out_receiver(sender, request, user, **kwargs):
    LoginLog.objects.create(user=user, loggedIn=False)
