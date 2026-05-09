from django.shortcuts import render,redirect
from .forms import ServiceForm,ReviewForm
from .models import Service,ServiceImages,Review
from accounts.views import loginpage
from company.models import Company
from company.views import dashboard,myservices
from django.db.models import Q
import ollama
from ollama import chat
from django.contrib import messages
# Create your views here.

def add_service(request):
    company = Company.objects.get(company_admin = request.user)
    if request.method == 'POST':
        form = ServiceForm(request.POST,request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.company = company
            if not service.description:
                response1 = ollama.chat(model='llama3.2:latest',messages=[
                    {
                    'role':'user',
                    'content':f"""
                    You are a professional business consultant for UAE based service marketplace,
                    write a comprehensive entry for the service:{service.title},
                    do not add description and service name as heading just give description,
                    write a 2 sentence marketing summary focusing on quality and customer support,keep total under 120 words"""},

                ],
                options = {'temperature':0.7})
                service.description = response1.message.content
            if not service.overview:
                response2 = ollama.chat(model='llama3.2:latest',messages=[
                    {
                    'role':'user',
                    'content':f"""
                    You are a professional business consultant for UAE based service marketplace,
                    write a overview for the service:{service.title},
                    do not add overview as heading,
                    List 4 clear, professional steps involved in performing this service from start to finish,
                    in next line List 3 or 4 specific professional tools or products used for this service,
                    format the response clearly with headers."""},

                ],
                options = {'temperature':0.7})
                service.overview = response2.message.content
            service.save()
            return redirect(dashboard)
    else:
        form = ServiceForm()
    return render(request,'services/addservice.html',{'form':form})

def update_service(request,sid):
    service = Service.objects.get(id = sid)
    if request.method == 'POST':
        form = ServiceForm(request.POST,request.FILES,instance=service)
        if form.is_valid():
            form.save()
            return redirect(dashboard)
    else:
        form = ServiceForm(instance=service)
    return render(request,'services/addservice.html',{'form':form})

def delete_service(request,sid):
    service = Service.objects.get(id = sid)
    service.delete()
    return redirect(dashboard)

def service_view(request,sid):
    service = Service.objects.get(id = sid)
    reviews = Review.objects.filter(service__id = sid)
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ReviewForm(request.POST,request.FILES)
            if form.is_valid():
                review = form.save(commit=False)
                review.service = service
                review.user = request.user
                review.save()
                return redirect(service_view,sid = sid)
        else:
            return redirect(loginpage)
    else:
        form = ReviewForm
    return render(request,'services/service.html',{'service':service,'reviews':reviews,'form':form})

def searchpage(request):
    query = request.GET.get('search')
    results = []

    if query:
        results = Service.objects.filter(Q(title__icontains = query) | Q(description__icontains = query),is_available = True)
    return render(request,'services/search.html',{'results':results,'query':query})

def add_serviceimages(request,sid):
    service = Service.objects.get(id = sid)
    if request.method == 'POST':
        images = request.FILES.getlist('gallery_images')
        for img in images:
            ServiceImages.objects.create(service = service,images = img)
        messages.success(request,f" Your service images added successfully")
        return redirect(myservices)
    return render(request,'services/add_images.html',{'service':service})



