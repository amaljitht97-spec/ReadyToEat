from django.contrib import admin
from donor.models import FoodCategory,FoodDonorModel

# Register your models here.
admin.site.register(FoodCategory)
admin.site.register(FoodDonorModel)