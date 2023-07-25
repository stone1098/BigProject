from django.db import models
from accounts.models import User

# Create your models here.


class CarTextInput(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accident_report = models.TextField(max_length=600)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text_id
    
class CarTextOutput(models.Model):
    car_text_id = models.ForeignKey(CarTextInput, on_delete=models.CASCADE)
    result = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.car_text_id