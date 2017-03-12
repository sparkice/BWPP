from django import forms
from .models import User,Mail


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'username',
            'placeholder': '用户名'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'password',
            'placeholder': '密码'}))


class RegisterForm(forms.Form):
    username = forms.CharField(label='username',
                               max_length=50,
                               widget=forms.TextInput(attrs={'id': 'username','onclick': 'authentication()'}))
    userID = forms.CharField(label='userID',
                               max_length=10,
                               widget=forms.TextInput(attrs={'id': 'userID', 'onclick': 'authentication()'}))
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

class RePassForm(forms.Form):
    old_pd = forms.CharField(widget=forms.PasswordInput)

    new_pd = forms.CharField(widget=forms.PasswordInput)