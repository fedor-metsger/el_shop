
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.forms import ModelForm, Form


class UserLoginForm(AuthenticationForm):
    pass
    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'User name', 'id': 'emailPost'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password', 'id': 'passwordPost'}))

# class UserRegisterForm(UserCreationForm):
#     pass
#
#
# class UserPasswordForm(ModelForm):
#     pass
#
#
# class ProductListForm(Form):
#     pass
#
#
# class ProductUpdateForm(Form):
#     pass
#
#
# class BasketListForm(Form):
#     pass
