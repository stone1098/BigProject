from django.db import models
from accounts.models import User

# Create your models here.

class CarImageInput(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='images/repair_cost/input')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.img_id
    
class CarImageOutput(models.Model):
    car_image_id = models.ForeignKey(CarImageInput, on_delete=models.CASCADE)
    car_company = models.CharField(max_length=20, null=True)
    car_type = models.CharField(max_length=20, null=True)
    car_year = models.CharField(max_length=20, null=True)
    result_img = models.ImageField(blank=True, upload_to='images/repair_cost/result')
    result_part = models.JSONField(null=True)
    result_cost = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.car_image_id

