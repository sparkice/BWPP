from captcha.fields import CaptchaField
from django import forms


class CaptchaTestForm(forms.Form):
    captcha = CaptchaField(label='captcha')  # 为生成的验证码图片，以及输入框
    username = forms.CharField(label='username',
                               max_length=50,
                               widget=forms.TextInput(
                                   attrs={'id': 'username', 'onclick': 'authentication()', 'class': 'form-control','placeholder': '用于稍后我们的短信验证'}))
    userID = forms.CharField(label='userID',
                             max_length=10,
                             widget=forms.TextInput(
                                 attrs={'id': 'userID', 'onclick': 'authentication()', 'class': 'form-control',}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


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
                               widget=forms.TextInput(attrs={'id': 'username', 'onclick': 'authentication()'}))
    userID = forms.CharField(label='userID',
                             max_length=10,
                             widget=forms.TextInput(attrs={'id': 'userID', 'onclick': 'authentication()'}))
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    captcha = CaptchaField()


class MailForm(forms.Form):
    whereup = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'weui-input',
                'id': 'mail_whereup'
            }
        )
    )

    wheredown = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'weui-input',
                'id': 'mail_wheredown'
            }
        )
    )

    detail = forms.CharField(
        required=False, widget=forms.TextInput(
            attrs={
                'class': 'weui-textarea',
                'id': 'mail_detail',
                'height': 20,
            }
        )
    )


class RePassForm(forms.Form):
    old_pd = forms.CharField(widget=forms.PasswordInput)
    new_pd = forms.CharField(widget=forms.PasswordInput)


class CheckForm(forms.Form):
    sms_check = forms.IntegerField(label='sms_check', widget=forms.TextInput(
        attrs={'id': 'sms_check', 'class': 'form-control', 'placeholder': '输入之前你收到的短信验证码'
               }))
    updatephoto = forms.ImageField(label='updatephoto', max_length=100)
