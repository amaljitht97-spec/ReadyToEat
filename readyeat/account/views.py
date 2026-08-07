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

        form=RegisterForm()

        return render(request,"signup.html",{"form":form})

    def post(self,request):

        form=RegisterForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request,"Registration Successful")

            return redirect("login")

        return render(request,"signup.html",{"form":form})
    
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib import messages
from account.forms import UserLoginForm

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from account.forms import UserLoginForm

class LoginView(View):

    def get(self, request):
        form = UserLoginForm()
        next_page = request.GET.get("next")
        return render(request, "login.html", {
            "form": form,
            "next": next_page
        })

    def post(self, request):

        form = UserLoginForm(request.POST)
        next_page = request.POST.get("next")

        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is None:
                messages.error(request, "Invalid username or password.")
                return render(request, "login.html", {
                    "form": form,
                    "next": next_page
                })

            login(request, user)

            # Admin
            if user.is_superuser:
                return redirect("/admin/")

            # Donor button clicked
            if next_page == "donor":

                if user.role == "donor":
                    return redirect("donorprofile")

                logout(request)
                messages.error(request, "Only Donor accounts can access this page.")
                return redirect("login")

            # Customer button clicked
            if next_page == "customer":

                if user.role == "customer":
                    return redirect("customerprofile")

                logout(request)
                messages.error(request, "Only Customer accounts can access this page.")
                return redirect("login")

            # Normal login
            if user.role == "donor":
                return redirect("donorprofile")

            elif user.role == "customer":
                return redirect("customerprofile")

            logout(request)
            messages.error(request, "Role not assigned.")
            return redirect("login")

        return render(request, "login.html", {
            "form": form,
            "next": next_page
        })


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
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View

class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect("homedash")

    def post(self, request):
        logout(request)
        return redirect("homedash")