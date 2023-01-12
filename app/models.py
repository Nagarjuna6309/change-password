from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    address=models.TextField(max_length=1000)
    profile_pic=models.ImageField()