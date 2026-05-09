from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class customuserAdmin(UserAdmin):
    list_display = ('username','email','role','verified','is_staff')
    list_filter = ('role','verified','is_staff')
    fieldsets = UserAdmin.fieldsets + (('marketplace info',{'fields':('role','phone_no','verified','profile_pic')}),)
    add_fieldsets =  UserAdmin.fieldsets + ((None,{'fields':('role','phone_no','verified','profile_pic')}),)

admin.site.register(CustomUser,customuserAdmin)
