
from django.core.mail import send_mail

def send_verification_email(user_email, code):
    send_mail(
        subject="رمز التفعيل لحسابك",
        message=f"رمز التفعيل الخاص بك هو: {code}",
        from_email="noreply@example.com",
        recipient_list=[user_email],
        fail_silently=False,
    )
