from django.core.exceptions import ObjectDoesNotExist
from celery import Celery, shared_task
from celery.signals import task_failure
from django.core.mail import send_mail
from django.conf import settings
from .models import MyData, CustomerData

app = Celery('your_project_name')  # Replace 'your_project_name' with your actual project name

class StopCeleryTask(Exception):
    pass
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

@shared_task
def task_one():
    try:
        # Increment the MyData number field by 1
        number = MyData.objects.get(id=1)
        

        try:
            customer_data = CustomerData.objects.get(id=number.number)
            # email_to_list = [customer_data.Email]
            # subject = " Boost Your LinkedIn Network with Our Free Chrome Extension"
            # message = f"Hey {customer_data.name}, my name is MAjid. I am just sending an email for testing purpose."
            # email_from = settings.EMAIL_HOST_USER
            # send_mail(subject, message, email_from, email_to_list)
            # customer_data.status = "Success Again"
            # customer_data.save()
            # number.number += 1
            # number.save()
            # print("Email sent successfully")

            d = {
                'user_first_name': customer_data.name,
            }


            newList = [customer_data.Email]
            plaintext = get_template('emails/email.txt')
            htmly = get_template('emails/activate_template.html')
            subject, from_email = 'Boost Your LinkedIn Network with Our Free Chrome Extension', settings.EMAIL_HOST_USER
            text_content = plaintext.render(d)
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(
                subject, text_content,  from_email, to=newList)
            msg.attach_alternative(html_content, "text/html")
            try:
                msg.send()
                customer_data.status = "Success Again"
                customer_data.save()
                number.number += 1
                number.save()
                print("Email sent successfully")
            except Exception as e:
                print(f"Email sending failed with error: {e}")



        except ObjectDoesNotExist:
            # Customer data not found, raise a custom exception to stop the Celery task
            email_to_list = ["mj2webupload@gmail.com"]
            subject = "Warning"
            message = f"Hey MAjid. celery stopped."
            email_from = settings.EMAIL_HOST_USER

            send_mail(subject, message, email_from, email_to_list)
            raise StopCeleryTask("Customer data not found")

    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        raise  # Re-raise the exception to stop the task

@task_failure.connect
def handle_task_failure(sender, **kwargs):
    exception = kwargs.get('exception')
    if isinstance(exception, StopCeleryTask):
        sender.revoke(terminate=True)  # Stop the Celery task
