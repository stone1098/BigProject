from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date

class User(AbstractUser):
    email = models.EmailField(unique=True)
    birthdate = models.DateField(null=True, default=date.today)
    address = models.CharField(max_length=200)
    create_date = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=11)
    def __str__(self):
        return self.username


class AuthSms(models.Model):
    phone_number = models.CharField(max_length=11, unique=True)
    auth_number = models.IntegerField()
    def __str__(self):
        return str(self.phone_number)
    class Meta:
        db_table = 'auth_sms'