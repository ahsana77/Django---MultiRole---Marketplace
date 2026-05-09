from django.shortcuts import render,redirect
from services.models import Service,Category,Offer,Sub_category
from .models import Cart,Bookings
from django.contrib import messages
from company.views import dashboard
from django.contrib.auth.decorators import login_required
# Create your views here.

# --------------- main page ----------

def homepage(request):
    categories = Category.objects.all().prefetch_related('sub_categories')
    nav_categories = categories[:4]
    offers = Offer.objects.all()
    recom_services = Service.objects.filter(is_available = True,company__verified = True)
    recom_services[:4]
    recent_services = Service.objects.filter(is_available = True,company__verified = True).order_by('-id')[:4]

    context = {
        'recommended_services':recom_services,
        'categories':categories,
        'offers':offers,
        'nav_categories':nav_categories,
        'recent_services':recent_services,
    }

    return render(request,'booking/home.html',context)



def offer_detail(request,offid):
    offer = Offer.objects.get(id = offid)
    services = Service.objects.filter(category = offer.applicable_cat,is_available = True)
    return render(request,'booking/offer.html',{'offer':offer,'services':services,'offers':offer})


def category_view(request,cid):
    category = Category.objects.get(id = cid)
    sub_cats = Sub_category.objects.filter(category = category).prefetch_related('subcat_services')

    context = {
        'category':category,        
        'subcategories':sub_cats,
    }
    return render(request,'booking/cat_view.html',context)

def allcats_view(request):
    categories = Category.objects.all()
    return render(request,'booking/allcats.html',{'categories':categories})

@login_required(login_url='login')
def add_cart(request,sid):
    if request.method == 'POST':
        service = Service.objects.get(id = sid)
        selected_date = request.POST.get('booking_date')
        selected_slot = request.POST.get('timeslot')
        exist = Cart.objects.filter(
            user = request.user,
            service = service,
            date = selected_date,
            timeslot = selected_slot
        ).exists()

        if exist:
            messages.warning(request,f"you have already scheduled this {service.title} for this time.")
        else:
            Cart.objects.create(
                user = request.user,
                service = service,
                date = selected_date,
                timeslot = selected_slot,
                quantity = 1

            )
            messages.success(request,f"{service.title} added to your cart!")
        return redirect(cart_view)


@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user = request.user)
    promo_code  = request.GET.get('promo_code')
    discount_amount = 0
    total = 0
    for item in cart_items:
        total += item.service.price * item.quantity
    if promo_code:
        try:
            offer = Offer.objects.get(code = promo_code)
            discount_amount = (total * offer.discount_percent)/100
            total = total - discount_amount
            messages.success(request,f"Code '{promo_code}' applied ! Saved AED {discount_amount}")
        except Offer.DoesNotExist:
            messages.error(request,'Invalid')

    # to apply offer

    return render(request,'booking/cart_view.html',{'cart_items':cart_items,'total':total,'discount':discount_amount,'promo':promo_code})


def confirm_booking(request):
    cart_items = Cart.objects.filter(user = request.user)
    if not cart_items.exists():
        messages.error(request,'your  cart is empty!')
        return redirect(cart_view)

    promo_code = request.GET.get('promo_code')
    discount_perc = 0
    if promo_code:
        offer = Offer.objects.get(code = promo_code)
        discount_perc = offer.discount_percent
    for item in cart_items:
        service_owner = item.service.company.company_admin
        if service_owner.role == 'freelancer':
            assigned_worker = service_owner
        else:
            assigned_worker = None
        final_price = item.service.price
        if discount_perc > 0:
            final_price -= (final_price*discount_perc/100)
        Bookings.objects.create(
            customer = request.user,
            service = item.service,
            company = item.service.company,
            assigned_to = assigned_worker,
            booking_date = item.date,
            service_price = final_price,
            timeslot = item.timeslot,
            status = 'pending'
        )
    cart_items.delete()
    messages.success(request,"Booking successful!")
    return redirect(cart_view)
        

def remove_cart(request,cartid):
    cart_item = Cart.objects.get(id = cartid,user = request.user)
    cart_item.delete()
    messages.success(request,'service removed from your schedule')
    return redirect(cart_view)


def booking_status_update(request,bookid,new_status):
    booking = Bookings.objects.get(id = bookid)

    booking.status = new_status
    booking.save()
    return redirect(dashboard)



