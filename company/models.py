from django.db import models
from django.conf import settings
# Create your models here.

class Company(models.Model):
    company_admin = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='owned_company')
    name = models.CharField(max_length=100)
    des = models.TextField(blank=True)
    logo = models.ImageField(upload_to='company_logo',blank=True,null=True)
    address = models.CharField(max_length=500,blank=True)
    verified = models.BooleanField(default=False)
    STATUS_CHOICES = [
        ('pending','Pending'),
        ('approved','Approved'),
        ('rejected','Rejected')
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')

    def __str__(self):
        return self.name
    
class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='emp_profile')
    img = models.ImageField(upload_to='emp_pic',null=True,blank=True)
    company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name='company_emp')
    designation = models.CharField(max_length=100,blank=True,null=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


