from sample_app.celery import app
from django.conf import settings
from django.core.mail import send_mail
from random import randint

@app.task
def task_one():
    try:
        email_to_list = ["mj2webupload@gmail.com"]
        subject = "Check Celery"
        otp = randint(1000, 9999)

        message = f"Your One Time Password for verification is: {otp}"

        email_from = settings.EMAIL_HOST_USER

        send_mail(subject, message, email_from, email_to_list)

        print("Email sent successfully")
    except Exception as e:
        print(f"Failed: {str(e)}")
        return "Failed"
@app.task
def task_two(data, *args, **kwargs):
    print(f" task two called with the argument {data} and worker is running good")
    return "success"
