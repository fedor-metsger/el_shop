
# from django.forms import models, forms, BaseInlineFormSet
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.core.exceptions import ValidationError
from django.forms import ModelForm, Form

from backend.models import Product, User, Shop, ProductInfo


# class ProductForm(forms.models.ModelForm):
#     class Meta:
#         model = Product
#         fields = "__all__"
#         # exclude = ("creation_date", "modification_date", "owner")

class UserLoginForm(AuthenticationForm):
    pass
    # def __init__(self, *args, **kwargs):
    #     super(UserLoginForm, self).__init__(*args, **kwargs)
    #
    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'User name', 'id': 'emailPost'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password', 'id': 'passwordPost'}))

class UserRegisterForm(UserCreationForm):
    pass
    # class Meta:
    #     model = User
    #     fields = ("username", "password1", "password2", "email", "company", "position", "type")

    # def __init__(self, *args, **kwargs):
    #     super(UserRegisterForm, self).__init__(*args, **kwargs)
    #
    # username = UsernameField(widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder': 'User name', 'id': 'userNamePost'}))
    # password1 = forms.CharField(widget=forms.PasswordInput(
    #     attrs={'class': 'form-control', 'placeholder': 'Password', 'id': 'password2Post'}))
    # password2 = forms.CharField(widget=forms.PasswordInput(
    #     attrs={'class': 'form-control', 'placeholder': 'Password', 'id': 'passwordPost'}))
    # email = forms.CharField(widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder': 'e-mail', 'id': 'emailPost'}))
    # company = forms.CharField(widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder': 'Company', 'id': 'companyPost'}))
    # position = forms.CharField(widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder': 'Position', 'id': 'positionPost'}))
    # CHOICES = [("customer", "Покупатель"), ("backend", "Магазин")]
    # type = forms.ChoiceField(widget=forms.Select(
    #     attrs={'class': 'form-control', 'id': 'typePost'}),
    #     choices=CHOICES
    # )

class UserPasswordForm(ModelForm):
    pass
    # class Meta:
    #     model = User
    #     fields = ["username", "email"]

# class UserActivationForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ()
#     user_code = forms.CharField(max_length=20,
#                                 label="Введите код из письма, присланного после регистрации:")


class ProductListForm(Form):
    pass
    # url = forms.CharField(widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder': 'http://link.to.file.yaml', 'id': 'URL'}))


class ProductUpdateForm(Form):
    pass
    # def __init__(self, *args, **kwargs):
    #     super(UserLoginForm, self).__init__(*args, **kwargs)

    # url = forms.CharField(widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder': 'http://link.to.file.yaml', 'id': 'URL'}))


class BasketListForm(Form):
    pass