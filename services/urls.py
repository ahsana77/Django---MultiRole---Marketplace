from django.urls import path
from .views import *
urlpatterns = [
    path('addservice',add_service,name='addservice'),
    path('updateservice/<int:sid>',update_service,name='updateservice'),
    path('deleteservice/<int:sid>',delete_service,name = 'deleteservice'),
    path('service/<int:sid>',service_view,name='serviceview'),
    path('search',searchpage,name='search'),
    path('serviceimages/<int:sid>',add_serviceimages,name='addgallery')
]