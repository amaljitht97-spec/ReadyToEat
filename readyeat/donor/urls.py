from django.urls import path
from donor.views import *

urlpatterns=[
    path('registerdonor',DonorSignupView.as_view(),name="registerdonr"),
    path('donorprofile',DonorProfileView.as_view(),name="donorprofile"),
    # path('foodscategori',FoodCategoryViews.as_view(),name="foodscat"),
    path('fooditems',FoodItemsCreateView.as_view(),name="fooditems"),
    path('fooddonor',DonorFoodView.as_view(),name="fooddonor"),
    path('fooddelete/<int:pk>',DeleteDonorFoodView.as_view(),name="fooddelete"),
    path('updatedonor/<int:pk>',UpdateDonorView.as_view(),name="updatedonor"),


]