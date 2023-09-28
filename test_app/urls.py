from django.urls import path
from .views import *

urlpatterns = [
    # Other URL patterns...
    path('send-verification-email/', send_verification_email, name='send_verification_email'),
]