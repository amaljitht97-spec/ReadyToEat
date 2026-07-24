from django import forms
from account.models import User
from django.contrib.auth.forms import UserCreationForm
from customer.models import *

# forms

class CustomerRegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=["email","username","phone","password1","password2"]
    def save(self, commit = True):
        customer=super().save(commit=False)
        customer.role="customer"
       
        if commit:
            customer.save()
        return customer
    
class CustomerForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=["phone","address"]

class FoodRequestForm(forms.ModelForm):
    class Meta:
        model=FoodRequestModel
        fields=["food","user","quantity","status",]

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["comment", "rating"]