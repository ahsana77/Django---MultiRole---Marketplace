from django import forms
from .models import Service,Review

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title','category','sub_cat','img','description','overview','price','duration_minutes','is_available']

        widgets = {'title':forms.TextInput(attrs={'class':'form-control'}),
                   'category':forms.Select(attrs={'class':'form-control'}),
                   'sub_cat':forms.Select(attrs={'class':'form-control'}),
                   'img':forms.ClearableFileInput(attrs={'class':'form-control'}),
                   'description':forms.Textarea(attrs={'class':'form-control','rows':3}),
                   'overview':forms.Textarea(attrs={'class':'form-control'}),
                   'price':forms.NumberInput(attrs={'class':'form-control'}),
                   'duration_minutes':forms.NumberInput(attrs={'class':'form-control'}),
                   'is_availabe':forms.CheckboxInput(attrs={'class':'form-check-input'}),

                   }
        


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating','comment','img']

        widgets = {
            'rating':forms.NumberInput(attrs = {'class':'form-control', 'min':1,'max':5}),
            'comment':forms.Textarea(attrs={'class':'form-control','rows':3}),
            'img':forms.FileInput(attrs={'class':'form-control'})
        }