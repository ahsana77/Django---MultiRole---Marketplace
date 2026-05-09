from django.urls import path
from .views import *

urlpatterns=[
    path('addcompany',create_company,name='addcomp'),
    path('dashboard',dashboard,name='dashboard'),
    path('emp_allocate/<int:bookid>',allocate_job,name='allocatejob'),
    path('myteam',my_team,name='myteam'),
    path('addemp',add_emp,name='addemp'),
    path('myservice',myservices,name='myservice'),
    path('remove_emp/<int:empid>',remove_emp,name='removeemp'),
    path('emptasks/<int:empid>',emp_tasks,name='emptasks'),
    path('settings',settings,name='settings')


]