from django.contrib import admin
from .models import Service,Category,Offer,Sub_category,Review,ServiceImages
# Register your models here.
admin.site.register(Service)
admin.site.register(Category)
admin.site.register(Offer)
admin.site.register(Sub_category)
admin.site.register(Review)
admin.site.register(ServiceImages)