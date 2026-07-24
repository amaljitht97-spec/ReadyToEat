from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.views import View
from account.forms import *
from django.contrib import messages
from django.views.generic import FormView
from django.contrib.auth import authenticate,login
from django.urls import reverse_lazy,reverse
# Create your views here.

class HomeDashView(View):
    def get(self,request):
        return render(request,"Homedash.html")

class SignupView(View):
    def get(self,request):
       form=UserForm
       return render(request,"signup.html",{"form":form})
    def post(self,request):
        form_data=UserForm(data=request.POST)
        if form_data.is_valid():
            form_data.save()
            messages.success(request,"admin registration successfully!")
            return redirect('/admin/')
        messages.info(request,"invalid input!")
        return render(request,"signup.html",{"form":form_data})
    


class LoginView(View):

     def get(self, request):
         form = UserLoginForm()
         return render(request, "login.html", {"form": form})

     def post(self, request):
         form_data = UserLoginForm(data=request.POST)

         if form_data.is_valid():
             uname = form_data.cleaned_data.get("username")
             pswd = form_data.cleaned_data.get("password")

             user = authenticate(request, username=uname, password=pswd)
             if user is not None:
               login(request, user)

             if user is not None:
                 login(request, user)

                 # Admin check
                 if user.is_superuser:
                     return redirect('/admin/')

                 # Role-based redirect
                 if user.role=="donor":
                     return redirect('donorprofile')
                 elif user.role == "customer":
                     return redirect('customerprofile')
                 else:
                     messages.warning(request, "User role not assigned!")
                     return redirect('login')
             else:
              messages.warning(request, "Invalid Credentials!")
              return redirect('login')
#         #    
# 
#  if user is not None:
#         #        login(request, user)

#         #        if user.is_superuser:
#         #          return redirect('/admin/')

#         #     role = user.role.lower() if user.role else ""

#         #     if role == "donor":
#         #       return redirect('donorprofile')
#         #     elif role == "customer":
#         #       return redirect('customerprofile')
#         #     else:
#         #       messages.warning(request, "User role not assigned!")
#         #     return redirect('login')
#       

#         # return render(request, "login.html", {"form": form_data})

# class LoginView(View):

#     def get(self, request):
#         form = UserLoginForm()
#         return render(request, "login.html", {"form": form})

#     def post(self, request):
#         form_data = UserLoginForm(data=request.POST)

#         if form_data.is_valid():
#             uname = form_data.cleaned_data.get("username")
#             pswd = form_data.cleaned_data.get("password")

#             user = authenticate(request, username=uname, password=pswd)

#             if user is not None:
#                 login(request, user)

#                 # Admin
#                 if user.is_superuser:
#                     return redirect('/admin/')

#                 # Role check
#                 if hasattr(user, 'role'):
#                     role = user.role.lower()

#                     if role == "donor":
#                         return redirect('donorprofile')

#                     elif role == "customer":
#                         return redirect('customerprofile')

#                 messages.warning(request, "User role not assigned!")
#                 return redirect('login')

#             else:
#                 messages.warning(request, "Invalid credentials!")
#                 return redirect('login')

#         return render(request, "login.html", {"form": form_data})
  