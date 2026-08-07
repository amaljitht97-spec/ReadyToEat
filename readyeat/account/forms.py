from django import forms
from django.contrib.auth.forms import UserCreationForm
from account.models import User

class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "phone",
            "role",
            "password1",
            "password2",
        ]

    def __init__(self,*args,**kwargs):

        super().__init__(*args,**kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                "class":"w-full border rounded-lg px-4 py-3"
            })

    def save(self,commit=True):

        user = super().save(commit=False)

        if user.role=="donor":
            user.is_staff=True

        if commit:
            user.save()

        return user
class UserLoginForm(forms.Form):
    username=forms.CharField(max_length=100)
    password=forms.CharField(max_length=100)