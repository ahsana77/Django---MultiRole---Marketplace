from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from services.models import Offer


class CustomuserRegform(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username','email','role','phone_no','profile_pic']



class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['title','code','discount_percent','applicable_cat','banner_img']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username','email','phone_no','profile_pic']