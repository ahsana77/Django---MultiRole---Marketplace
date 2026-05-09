from django.shortcuts import render,redirect
from .forms import companyCreationForm
from .models import Company,Employee
from services.models import Service
from booking.models import Bookings
from django.db.models import Sum
from accounts.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

def create_company(request):
    if request.user.role not in ['company admin','freelancer']:
        return redirect('/')
    if hasattr(request.user,'owned_company'):
        return redirect('/')
    if request.method == 'POST':
        form = companyCreationForm(request.POST,request.FILES)
        if form.is_valid():
            company = form.save(commit=False)
            company.company_admin = request.user
            company.save()
            if request.user.role == 'freelancer':
                Employee.objects.create(user = request.user, company = company, designation = 'Freelancer')
            return redirect(dashboard)
    else :
        # to show prefilled company name if it is freelancer
        initial_data = {}
        if request.user.role == 'freelancer':
            initial_data['name'] = f"{request.user.username}'s Services"
        form = companyCreationForm(initial = initial_data)
    return render(request,'company/create_company.html',{'form':form})


# --------Dashboard---------
def dashboard(request):
    user = request.user
    context = {}
    if user.role in ['company admin','freelancer']:
        try:
            company = Company.objects.get(company_admin = request.user)
            bookings = Bookings.objects.filter(company = company).order_by('-booking_date')
            employees = Employee.objects.filter(company = company)
            services = Service.objects.filter(company = company)
            completed_services = Bookings.objects.filter(company = company,status ='completed')
            price_list = completed_services.values_list('service_price',flat = True)
            total_sum = sum(price_list)
            if total_sum:
                total_earnings = total_sum
            else:
                total_earnings = 0

            active_services_count = services.filter(is_available = True).count()

            context = {'company':company,
                    'employee':employees,
                    'services':services,
                    'bookings':bookings,
                    'total_earnings':total_earnings,
                    'active_services_count':active_services_count,}

        except Company.DoesNotExist:
            redirect(create_company)
        
    elif user.role == 'employee':
        bookings = Bookings.objects.filter(assigned_to = user).order_by('-booking_date')
        context = {
            'bookings':bookings,
            'is_employee':True
        }

    # elif user.is_superuser:


    return render(request,'company/dashboard.html',context)



def allocate_job(request,bookid):
    if request.method == 'POST':
        booking = Bookings.objects.get(id = bookid)
        emp_user_id = request.POST.get('employee_id')
        if emp_user_id:
            worker = CustomUser.objects.get(id = emp_user_id)
            booking.assigned_to = worker
            booking.status = 'pending'
            booking.save()
            messages.success(request,f"successfully allocated to {worker.first_name}")
        else:
            messages.error(request,f"please select a valid employee")
        return redirect('dashboard')


@login_required
def my_team(request):
    company = Company.objects.get(company_admin = request.user)
    #company_emp is related_name
    employees = Employee.objects.filter(company = company)
    return render(request,'company/myteam.html',{'company':company,'employees':employees})

@login_required
def add_emp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        password = request.POST.get('password')
        emp_designation = request.POST.get('designation')
        img = request.FILES.get('profile')

        new_user = CustomUser.objects.create(username = email,
                                             email = email,
                                             first_name = name,
                                             password = password,
                                             role = 'employee')
        
        company = Company.objects.get(company_admin = request.user)
        Employee.objects.create(user = new_user,
                                img = img,
                                company = company,
                                designation = emp_designation)
        
        messages.success(request,f"Employee {name} added to {company.name}")
        return redirect(my_team)
    

def myservices(request):
    company = Company.objects.get(company_admin = request.user)
    services = Service.objects.filter(company = company)

    return render(request,'company/myservice.html',{'services':services})


def remove_emp(request,empid):
    employee = Employee.objects.get(id = empid)
    if employee.company.company_admin == request.user:
        user = employee.user
        employee.delete()
        user.delete()
        messages.success(request,f"staff {employee.user.first_name} removed !")
    return redirect(my_team)

def emp_tasks(request,empid):
    employee = Employee.objects.get(id = empid)
    tasks = Bookings.objects.filter(assigned_to = employee.user).order_by('-booking_date')

    return render(request,'company/emp_tasks.html',{'employee':employee,'tasks':tasks})



def settings(request):
    company = Company.objects.get(company_admin = request.user)
    if request.user == 'POST':
        form = companyCreationForm(request.POST,request.FILES,isinstance = company)
        if form.is_valid():
            form.save()
            messages.success(request,'Business profile updated!')
            return redirect(settings)
    else:
        form = companyCreationForm(instance=company)

    return render(request,'company/settings.html',{'form':form,'company':company})

        