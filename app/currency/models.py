from django.db import models


class Rate(models.Model):
    buy = models.DecimalField(max_digits=10, decimal_places=2)
    sell = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField()
    type = models.CharField(max_length=3)
    source = models.CharField(max_length=255)


class ContactUs(models.Model):
    id = models.AutoField(primary_key=True)
    email_from = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
