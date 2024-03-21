from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,PasswordChangeForm
from django.contrib.auth.models import User

class Login(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': 'True', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'curent-password','class':'form-control'}))
class Registration(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'True','class':'form-control'}))
    email = forms.EmailField(widget= forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

# class PasswordReset(PasswordChangeForm):
#     pass