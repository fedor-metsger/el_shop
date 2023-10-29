
# from django.forms import models, forms, BaseInlineFormSet
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Product, User


class ProductForm(forms.models.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        # exclude = ("creation_date", "modification_date", "owner")

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "company", "position", "type")

class UserActivationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ()
    user_code = forms.CharField(max_length=20,
                                label="Введите код из письма, присланного после регистрации:")