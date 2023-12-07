from django.db import models


class Rate(models.Model):
    buy = models.DecimalField(max_digits=10, decimal_places=2)
    sell = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    currency_type = models.CharField(max_length=3)
    source = models.CharField(max_length=255)


class ContactUs(models.Model):
    contact_id = models.AutoField(primary_key=True)
    email_from = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()


class Source(models.Model):
    source_id = models.AutoField(primary_key=True)
    source_url = models.CharField(max_length=255)
    source_name = models.CharField(max_length=64)
