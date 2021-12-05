from django.core.mail import send_mail
from django.conf import settings


def send_mail_after_registration(email, token):
    subject = 'Your account needs to be verified'
    message = f'Hi click on the link to verify you account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email])


def send_mail_after_forgot(email, token):
    subject = 'Your Forgot password link'
    message = f'Hi click on the link to reset your password http://127.0.0.1:8000/changepassword/{token}'
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email])
