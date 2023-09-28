from django.conf import settings
from django.core.mail import send_mail
from random import randint
from django.http import HttpResponse

def send_verification_email(request):
    try:
        email_to_list = ["mj2webupload@gmail.com"]
        subject = "Check Celery"
        otp = randint(1000, 9999)

        message = f"Your One Time Password for verification is: {otp}"

        email_from = settings.EMAIL_HOST_USER

        send_mail(subject, message, email_from, email_to_list)

        print("Email sent successfully")
        return HttpResponse("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return HttpResponse("Failed to send email")