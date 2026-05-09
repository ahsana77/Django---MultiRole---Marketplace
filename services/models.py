from django.db import models
from company.models import Company
from accounts.models import CustomUser
from django.db.models import Avg,Count
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='category_icons',blank=True)

    def __str__(self):
        return self.name
    
class Sub_category(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='sub_categories')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Service(models.Model):
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,related_name='cat_services')
    sub_cat = models.ForeignKey(Sub_category,on_delete=models.CASCADE,related_name='subcat_services',blank=True,null = True)
    company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name='services')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True,null=True)
    overview = models.TextField(blank=True,null=True)
    img = models.ImageField(upload_to='service_images',null = True,blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    duration_minutes = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def avg_rating(self):
        avg = self.service_reviews.aggregate(Avg('rating'))['rating__avg']
        if avg is not None:
            return round(avg,1)
        return 0
    
    def review_count(self):
        return self.service_reviews.count()

    def __str__(self):
        return f"{self.title} - {self.company}"



class Review(models.Model):
    service = models.ForeignKey(Service,on_delete=models.CASCADE,related_name='service_reviews')
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)
    comment = models.TextField()
    img = models.ImageField(upload_to='review_pics',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    

class ServiceImages(models.Model):
    service = models.ForeignKey(Service,on_delete=models.CASCADE,related_name='gallery')
    images = models.ImageField(upload_to='service_gallery')



class Offer(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    code = models.CharField(max_length=10)
    discount_percent = models.IntegerField()
    banner_img = models.ImageField(upload_to='offers')

    applicable_cat = models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

