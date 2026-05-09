from django.urls import path
from .views import *
urlpatterns = [
    path('',homepage,name='home'),
    path('offer/<int:offid>',offer_detail,name='offer'),
    path('cat_view/<int:cid>',category_view,name='catview'),
    path('allcats',allcats_view,name='allcats'),
    path('addcart/<int:sid>',add_cart,name='addcart'),
    path('cart',cart_view,name='cartview'),
    path('cart_remove/<int:cartid>',remove_cart,name='cart_remove'),
    path('booking',confirm_booking,name='booking'),
    path('update_status/<int:bookid>/<str:new_status>',booking_status_update,name='status_update'),


]