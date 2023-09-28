from django.conf import settings
from django.core.mail import send_mail
from random import randint
from django.http import HttpResponse
import pandas as pd
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import MyData,CustomerData
from django.db import IntegrityError  # Import IntegrityError
from .tasks import task_one


def send_verification_email(request):
    try:
        number = MyData.objects.get(id=1)
        customer_data = CustomerData.objects.get(id=number.number)
        email_to_list = [customer_data.Email]
        subject = "Testing celery"

        message = f"Hey {customer_data.name}, my name is MAjid i am justing sedning a email for testing purpose."

        email_from = settings.EMAIL_HOST_USER

        send_mail(subject, message, email_from, email_to_list)
        customer_data.status = "Success"
        customer_data.save()
        number.number = number.number+1
        number.save()
        print("Email sent successfully")
        return HttpResponse("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return HttpResponse("Failed to send email")
    


def send_verification_email_view(request):
    try:
        # Queue the Celery task to send the verification email
        task_one.delay()

        return HttpResponse("Email task queued successfully")
    except Exception as e:
        print(f"Failed to queue email task: {str(e)}")
        return HttpResponse("Failed to queue email task")
    



def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Read the uploaded Excel file using pandas
            excel_data = pd.read_excel(request.FILES['file'])
            
            # Iterate over rows and save data to the database
            for index, row in excel_data.iterrows():
                try:
                    CustomerData.objects.create(
                        name=row['Name'],
                        Email=row['Email'],
                        status="Not Sended"
                        # Add other fields as needed
                    )
                except IntegrityError:
                    # Ignore rows with duplicate email addresses
                    pass
            return redirect('success')  # Redirect to a success page after upload
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


def success_view(request):
    # Your view logic here
    return render(request, 'success_template.html') 