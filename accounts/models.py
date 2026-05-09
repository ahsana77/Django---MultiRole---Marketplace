from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin','Admin'),
        ('customer','Customer'),
        ('freelancer','Freelancer'),
        ('company admin','Company Admin'),
        ('employee','Employee'),
    )
    role = models.CharField(max_length=20,choices=ROLE_CHOICES,default='customer')
    phone_no = models.CharField(max_length=15,blank=True,null=True)
    profile_pic = models.ImageField(upload_to='profiles',blank=True,null=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username