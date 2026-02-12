from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

def send_welcome_email(user):
    subject = 'Welcome to Book & Novel'
    message = render_to_string('emails/welcome_email.html', {
        'user': user,
    })
    send_mail(
        subject,
        '',  # Empty plain text, only HTML
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=message,
        fail_silently=False,
    )

def send_otp_email(user, otp):
    subject = 'OTP Verification - Book & Novel'
    message = render_to_string('emails/otp_email.html', {
        'user': user,
        'otp': otp,
    })
    send_mail(
        subject,
        '',  # Empty plain text, only HTML
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=message,
        fail_silently=False,
    )

def send_order_confirmation_email(user, order):
    subject = 'Order Confirmation - Book & Novel'
    message = render_to_string('emails/order_confirmation.html', {
        'user': user,
        'order': order,
    })
    send_mail(
        subject,
        '',  # Empty plain text, only HTML
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=message,
        fail_silently=False,
    )
