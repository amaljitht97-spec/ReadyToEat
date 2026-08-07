from django import forms
from account.models import User
from django.contrib.auth.forms import UserCreationForm
from donor.models import *
from account.models import *
from datetime import timedelta
from django.utils import timezone





    
# class DonorForm(forms.ModelForm):
#     class Meta:
#         model=DonorProfile
#         fields=["organization_name","phone","address"]

class DonorForm(forms.ModelForm):
    class Meta:
        model = DonorProfile
        fields = ["organization_name", "phone", "address", "latitude", "longitude"]

     


# class FoodItemForm(forms.ModelForm):
#     expiry_hours = forms.IntegerField(label="Expiry (hours)")
#     class Meta:
#         model=FoodDonorModel
#         fields=["food_items","food_title","food_description","food_images","quantity","is_free","price","available"]

from django import forms
from .models import FoodDonorModel

class FoodItemForm(forms.ModelForm):
    expiry_hours = forms.IntegerField(
        label="Expiry (Hours)",
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Enter expiry in hours"
        })
    )

    class Meta:
        model = FoodDonorModel
        fields = [
            "food_items",
            "food_title",
            "food_description",
            "food_images",
            "quantity",
            "is_free",
            "price",
            "available",
        ]

        widgets = {

            "food_items": forms.Select(attrs={
                "class": "form-select"
            }),

            "food_title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter food title"
            }),

            "food_description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Enter food description"
            }),

            "food_images": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),

            "quantity": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter quantity"
            }),

            "price": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter price"
            }),

            "is_free": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),

            "available": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }
