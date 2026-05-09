from django.urls import path
from .views import *
urlpatterns=[
    path('register',registerpage,name='register'),
    path('login',loginpage,name='login'),
    path('logout',logoutpage,name='logout'),
    path('profile',customer_profile,name='profile'),
    path('admin',super_admin_dashboard,name='admin_dashboard'),
    path('verify_company/<int:compid>',verify_business,name='verify'),
    path('addoffer',add_offers,name='addoffer'),
    path('deloffer/<int:oid>',delete_offer,name='deleteoffer'),
    path('editpro',editprofile,name = 'editpro'),

]