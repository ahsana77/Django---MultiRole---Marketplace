from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from accounts.form import CustomuserRegform, OfferForm, UserUpdateForm
from booking.views import homepage
from company.views import create_company,dashboard
from booking.models import Bookings
from django.contrib.auth.decorators import login_required
from company.models import Company
from django.contrib import messages
from services.models import Service,Offer,Category

# Create your views here.
def registerpage(request):
    if request.method == 'POST':
        form  = CustomuserRegform(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            if user.role in ['company admin','freelancer']:
                return redirect(create_company)
            else:
                return redirect(loginpage)
    else:
        form = CustomuserRegform()
    return render(request,'accounts/register.html',{'form':form})

def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        passwrd = request.POST.get('psw')
        user = authenticate(request,username = username,password = passwrd)
        if user:
            login(request,user)
            if user.role == 'customer':
                return redirect(homepage)
            elif user.role in ['company admin','freelancer','employee']:
                return redirect(dashboard)
            elif user.role == 'admin':
                return redirect(super_admin_dashboard)
    return render(request,'accounts/login.html')

def logoutpage(request):
    logout(request)
    return redirect(loginpage)

@login_required
def customer_profile(request):
    my_bookings = Bookings.objects.filter(customer = request.user).order_by('-booking_date')
    context = {
        'bookings':my_bookings,
        'pending_count':my_bookings.filter(status = 'pending').count(),
        'confirmed_count' : my_bookings.filter(status='confirmed').count(),
    }
    return render(request,'accounts/profile.html',context)


@login_required
def super_admin_dashboard(request):
    companies = Company.objects.filter(company_admin__role = 'company admin').prefetch_related('company_emp')
    all_bookings = Bookings.objects.all()
    freelancers = Company.objects.filter(company_admin__role = 'freelancer')
    all_services = Service.objects.all()
    all_offers = Offer.objects.all()
    categories = Category.objects.all()

    completed_bookings = Bookings.objects.filter(status = 'completed')

    revenue = 0
    for booking in completed_bookings:
        revenue += booking.service_price

    platform_profit = float(revenue)*0.10

    all_companies = Company.objects.all()
    pending_verifications = all_companies.filter(verified = False).count()
    context = {
        'companies':companies,
        'freelancers':freelancers,
        'services':all_services,
        'categories':categories,
        'offers':all_offers,
        'bookings':all_bookings,
        'revenue':revenue,
        'profit':platform_profit,
        'pending_counts':pending_verifications,
    }
    return render(request,'accounts/super_dashboard.html',context)




def verify_business(request,compid):
    business = Company.objects.get(id = compid)
    business.verified = True
    business.save()
    messages.success(request,f"{business.name} is verified and live on homepage!")
    return redirect(super_admin_dashboard)

def add_offers(request):
    if request.method == 'POST':
        form = OfferForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Offer created successfiully")
            return redirect(super_admin_dashboard)
    else:
        form = OfferForm()
    return render(request,'accounts/addoffer.html',{'form':form})


def delete_offer(request,oid):
    offer = Offer.objects.get(id = oid)
    offer.delete()
    return redirect(super_admin_dashboard)


def editprofile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST,request.FILES,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(customer_profile)
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request,'accounts/editprofile.html',{'form':form})