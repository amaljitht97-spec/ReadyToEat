# """
# URL configuration for readyeat project.

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/6.0/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
# from django.contrib import admin
# from django.urls import path,include
# from account.views import *
# from donor.views import *
# from customer.views import *
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('donor/', include("donor.urls")),
#     path('customer/', include("customer.urls")),
#     path('', HomeDashView.as_view(), name="homedash"),
#     path('signup', SignupView.as_view(), name="signup"),
#     path('login', LoginView.as_view(), name="login"),
# ]

# #  ADD THIS BELOW (NOT INLINE)
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.contrib import admin
from django.urls import path, include
from account.views import HomeDashView, SignupView, LoginView,LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", HomeDashView.as_view(), name="homedash"),

    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
     path("logout/", LogoutView.as_view(), name="logout"),

    path("customer/", include("customer.urls")),
    path("donor/", include("donor.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)