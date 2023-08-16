from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class OrderForm(ModelForm):
    class Meta:
        model=Order
        fields='__all__'

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
 
class CustomerForm(ModelForm):
    class Meta:
        model=Customer
        fields='__all__'
        exclude=['user']               
class NewPasswordForm(forms.Form):
    
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput)



