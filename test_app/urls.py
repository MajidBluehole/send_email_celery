from django.urls import path
from .views import *

urlpatterns = [
    # Other URL patterns...
    path('send-verification-email/', send_verification_email, name='send_verification_email'),
    path('send_verification_email_view/', send_verification_email_view, name='send_verification_email_view'),
    path('upload/', upload_file, name='upload_file'),
    path('success/', success_view, name='success'),  # Replace 'views.success_view' with your actual success view.


]