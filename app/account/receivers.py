from account.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=User)
def check_user_phone(instance, **kwargs):
    instance.phone = ''.join(char for char in instance.phone if char.isdigit())
