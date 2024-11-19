from django import forms
from .models import Signup, Login, CartItem

class SignUpForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Signup
        fields = ['name','email','phone','password','confirm_password']
        widgets = {
            'password': forms.PasswordInput(),
        }

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']