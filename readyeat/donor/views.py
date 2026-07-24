from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.views import View
from donor.forms import *
from django.contrib import messages
from django.views.generic import *
from donor.models import *
from django.urls import reverse_lazy
from account.models import *

# Create your views here.

class DonorSignupView(View):
    def get(self,request):
       form=DonorRegistrationForm
       return render(request,"donorregistration.html",{"form":form})
    def post(self,request):
        form_data=DonorRegistrationForm(data=request.POST)
        if form_data.is_valid():
            form_data.save()
            messages.success(request,"admin registration successfully!")
            return redirect('homedash')
        messages.info(request,"invalid input!")
        return render(request,"donorregistration.html",{"form":form_data})
    
class DonorProfileView(View):

    def get(self, request):
        profile, created = DonorProfile.objects.get_or_create(
            user=request.user   
        )

        form = DonorForm(instance=profile)
        return render(request, "donorprofile.html", {"form": form})


    def post(self, request):
        profile, created = DonorProfile.objects.get_or_create(
            user=request.user   
        )

        form = DonorForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            return redirect('customerfoods')

        return render(request, "donorprofile.html", {"form": form})

class FoodCategoryViews(ListView):
    template_name="foods.html"
    queryset=FoodCategory.objects.all()
    context_object_name="data"




class FoodItemsCreateView(View):

    def get(self, request):
        form = FoodItemForm()
        return render(request, "fooditems.html", {"form": form})
    def post(self, request):
      form = FoodItemForm(request.POST, request.FILES)

      if form.is_valid():
        obj = form.save(commit=False)
        obj.donor = request.user

        hours = form.cleaned_data.get("expiry_hours")
        obj.expairy_time = timezone.now() + timedelta(hours=hours)  

        obj.save()
        return redirect('fooddonor')

      return render(request, "fooditems.html", {"form": form})
    
# class DonorFoodView(View):
#     def get(self,request):
#         donor=FoodDonorModel.objects.filter(donor=request.user)
#         return render(request,"donorfoodslist.html",{"data":donor})

class DonorFoodView(View):

    def get(self, request):
        donor = FoodDonorModel.objects.filter(donor=request.user)
        return render(request, "donorfoodslist.html", {"data": donor})

    # def post(self, request):
    #     print("POST received")  

    #     return redirect('fooddonor')

class DeleteDonorFoodView(View):
    def get(self,request,**kwargs):
        did=kwargs.get('pk')
        delete_profile=FoodDonorModel.objects.get(id=did)
        delete_profile.delete()
        return redirect('fooddonor')
class UpdateDonorView(View):
    def get(self,request,**kwargs):
        tid=kwargs.get('pk')
        donor=FoodDonorModel.objects.get(id=tid)
        form=FoodItemForm(instance=donor)
        return render(request,"donorupdatelist.html",{"form":form})
    def post(self,request,**kwargs):
        tid=kwargs.get('pk')
        donor=FoodDonorModel.objects.get(id=tid)
        form_data=FoodItemForm(data=request.POST,instance=donor,files=request.FILES)
        if form_data.is_valid():
          obj=form_data.save(commit=False)
          hours=form_data.cleaned_data.get("expiry_hours")
        if hours and hours > 0:
                obj.expairy_time = timezone.now() + timedelta(hours=hours)
                obj.available=True
                obj.save()
                messages.success(request,"Update Suceesssfully !")
                return redirect('fooddonor')
        return render(request,"donorupdatelist.html",{"form":form_data})


# from django.shortcuts import render, redirect, get_object_or_404
# from django.views import View
# from django.utils import timezone
# from datetime import timedelta
# from django.contrib import messages

# class UpdateDonorView(View):

#     def get(self, request, **kwargs):
#         tid = kwargs.get('pk')
#         donor = get_object_or_404(FoodDonorModel, id=tid)
#         form = FoodItemForm(instance=donor)
#         return render(request, "donorupdatelist.html", {"form": form})

#     def post(self, request, **kwargs):
#         tid = kwargs.get('pk')
#         donor = get_object_or_404(FoodDonorModel, id=tid)

#         form_data = FoodItemForm(
#             data=request.POST,
#             files=request.FILES,
#             instance=donor
#         )

#         if form_data.is_valid():
#             obj = form_data.save(commit=False)

#             hours = form_data.cleaned_data.get("expiry_hours")

#             if hours and hours > 0:
#                 obj.expairy_time = timezone.now() + timedelta(hours=hours)
#                 obj.available = True

#             

#             messages.success(request, "Updated successfully!")
#             return redirect('fooddonor')

#         return render(request, "donorupdatelist.html", {"form": form_data})