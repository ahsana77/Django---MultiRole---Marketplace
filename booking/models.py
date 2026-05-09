from django.db import models
from accounts.models import CustomUser
from services.models import Service
from company.models import Company
# Create your models here.
class Bookings(models.Model):
    STATUS_CHOICES = [
        ('pending','Pending'),
        ('confirmed','Confirmed'),
        ('completed','Completed'),
        ('cancelled','Cancelled'),
    ]

    customer = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='my_bookings')
    service = models.ForeignKey(Service,on_delete=models.CASCADE,related_name='service_booking')

    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    assigned_to  = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True,blank=True,related_name='jobs')

    service_price = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    booking_date = models.DateField()
    timeslot = models.CharField(max_length=50)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')

    def __str__(self):
        return f"{self.customer.username} - {self.service.title}"
    


class Cart(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    service = models.ForeignKey(Service,on_delete=models.CASCADE)
    date = models.DateField()
    timeslot = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.service.price * self.quantity
