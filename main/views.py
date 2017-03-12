from django import forms
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from . import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterForm, RePassForm
from django.core.exceptions import ObjectDoesNotExist


def register(request):
    if request.method == 'GET':
        rf = RegisterForm()
        return render(request, 'register.html', {'form': rf})
    if request.method == 'POST':
        rf = RegisterForm(request.POST)
        if request.POST.get('raw_username', '') != '':  # 不懂
            try:
                user = models.NewUser.objects.get(username=request.POST.get('raw_username', ''))
            except ObjectDoesNotExist:
                return render(request, 'register.html', {'form': rf, 'msg': "该用户名可用！"})
            else:
                return render(request, 'register.html', {'form': rf, 'msg': "该用户名已存在！"})
        else:
            if rf.is_valid():
                username = rf.cleaned_data['username']
                # userID = rf.cleaned_data['userID']
                filter_result1 = models.NewUser.objects.filter(username=username)
                # filter_result2 = models.NewUser.objects.filter(userID=userID)
                if len(filter_result1) > 0:  # 用户名(手机号码）或 学号 重名
                    return render(request, 'register.html', {'form': rf, 'msg': "该手机号或学号已存在！"})
                else:
                    username = rf.cleaned_data['username']
                    userID = rf.cleaned_data['userID']
                    password1 = rf.cleaned_data['password1']
                    password2 = rf.cleaned_data['password2']
                if password1 != password2:
                    return render(request, 'register.html', {'form': rf, 'msg': "输入密码不一致！"})
                else:
                    user = models.NewUser(username=username, password=password1)
                    user.set_password(password1)  # 重要！！！设置密码加密，不然是明文，admin里密码显示也是明文，登录不了
                    user.save()
                    u = models.UserProfile.objects.create(user=user, username=username,
                                                          userID=userID, password=password1,
                                                          userphone=username)  # 注册成功则创建对应user profile
                    u.save()
                    return redirect('/login', {'form': rf, 's': "注册成功！请登录！"})
            else:
                return render(request, 'register.html', {'form': rf, 'msg': "等待正确输入！"})


@login_required
def index(request):
    all_mails = models.Mail.objects.all()  # 在主页面中显示的快递
    mail = []
    for x in all_mails:
        if x.Situation == 0:  # 只显示没有被取的快递
            mail.append(x)

    return render(request, 'index.html', {'mails': mail})  # 返回字典


@login_required
def mailpage(request, mail_id):
    mail = models.Mail.objects.get(pk=mail_id)
    if mail.situation < 1:
        mail.Host = '选择领取后可见'
        mail.Phone = '选择领取后可见'
        mail.Host = '选择领取后可见'
        mail.date_time = '选择领取后可见'
    return render(request, 'mailpage.html', {'mail': mail})


@login_required
def editpage(request):
    return render(request, 'editpage.html')


@login_required
def editaction(request):
    NewWhereUP = request.POST.get('NewWhereUP', 'NEWWHEREUP')
    NewWhereDown = request.POST.get('NewWhereDown', 'NEWWHEREDOWN')
    NewWherePhone = request.POST.get('NewWherePhone', 'NEWPHONE')
    NeWWhereHost = request.POST.get('NewWhereHost', 'NEWHOST')
    models.Mail.objects.create(WhereUP=NewWhereUP, WhereDown=NewWhereDown, Phone=NewWherePhone, Host=NeWWhereHost)
    mails = models.Mail.objects.all()
    # return render(request,'index.html',{'mails': mails})
    return HttpResponseRedirect('http://127.0.0.1:8000')


class UserForm(forms.Form):
    username = forms.CharField()


@login_required
def user(request):
    return render(request, 'user.html')


@login_required
def take(request, mail_id):
    mail = models.Mail.objects.get(pk=mail_id)
    if mail.situation == 0:
        models.Mail.objects.get(pk=mail_id).situation = 1
    return HttpResponseRedirect('/')
