from django.db import models

class MyData(models.Model):
    number = models.IntegerField()


class CustomerData(models.Model):
    name = models.CharField(max_length=255)
    Email = models.CharField(max_length=25, unique=True)
    status = models.CharField(max_length=255)