from django import forms
from account.models import User
from django.contrib.auth.forms import UserCreationForm
from customer.models import *

# forms


    
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