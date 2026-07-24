from django import forms
from account.models import User
from django.contrib.auth.forms import UserCreationForm
from donor.models import *
from account.models import *
from datetime import timedelta
from django.utils import timezone





class DonorRegistrationForm(UserCreationForm):
    # exclude="role"
    class Meta:
        model=User
        fields=["email","username","phone","password1","password2"]
    def save(self, commit = True):
        donor=super().save(commit=False)
        donor.role="donor"
        donor.is_staff=True
        donor.is_active=True
       
        if commit:
            donor.save()
        return donor
    
# class DonorForm(forms.ModelForm):
#     class Meta:
#         model=DonorProfile
#         fields=["organization_name","phone","address"]

class DonorForm(forms.ModelForm):
    class Meta:
        model = DonorProfile
        fields = ["organization_name", "phone", "address", "latitude", "longitude"]

     


class FoodItemForm(forms.ModelForm):
    expiry_hours = forms.IntegerField(label="Expiry (hours)")
    class Meta:
        model=FoodDonorModel
        fields=["food_items","food_title","food_description","food_images","quantity","is_free","price","available"]
   
