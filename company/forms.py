from django import forms
from .models import Company

class companyCreationForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name','des','logo','address']
        labels = {
            'name':'Company Name',
            'des':'Tell us about your sevices',
        }


    def __init__(self, *args,**kwargs ):
        super().__init__(*args,**kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs.update({'class':'form-control'})
