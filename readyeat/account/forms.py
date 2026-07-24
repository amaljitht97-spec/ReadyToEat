from django import forms
from account.models import User
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):
    class Meta:
        model=User
        fields=["email","username","phone","role","password1","password2"]
    def save(self, commit = True):
        user=super().save(commit=False)
        user.is_superuser=True
        user.is_staff=True
        user.is_active=True
        user.role="admin"
        if commit:
            user.save()
        return user
    
class UserLoginForm(forms.Form):
    username=forms.CharField(max_length=100)
    password=forms.CharField(max_length=100)