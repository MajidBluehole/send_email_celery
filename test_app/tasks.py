from django.core.exceptions import ObjectDoesNotExist
from celery import Celery, shared_task
from celery.signals import task_failure
from django.core.mail import send_mail
from django.conf import settings
from .models import MyData, CustomerData

app = Celery('your_project_name')  # Replace 'your_project_name' with your actual project name

class StopCeleryTask(Exception):
    pass

@shared_task
def task_one():
    try:
        # Increment the MyData number field by 1
        number = MyData.objects.get(id=1)
        

        try:
            # Fetch the customer data
            customer_data = CustomerData.objects.get(id=number.number)

            # Prepare and send the email
            email_to_list = [customer_data.Email]
            subject = "Testing celery"
            message = f"Hey {customer_data.name}, my name is MAjid. I am just sending an email for testing purpose."
            email_from = settings.EMAIL_HOST_USER

            send_mail(subject, message, email_from, email_to_list)

            # Update the customer data status field
            customer_data.status = "Success"
            customer_data.save()
            number.number += 1
            number.save()

            print("Email sent successfully")
        except ObjectDoesNotExist:
            # Customer data not found, raise a custom exception to stop the Celery task
            raise StopCeleryTask("Customer data not found")

    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        raise  # Re-raise the exception to stop the task

@task_failure.connect
def handle_task_failure(sender, **kwargs):
    exception = kwargs.get('exception')
    if isinstance(exception, StopCeleryTask):
        sender.revoke(terminate=True)  # Stop the Celery task
