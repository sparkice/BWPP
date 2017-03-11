from django import forms
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from . import models
from django.contrib.auth.models import User

@login_required
def index(request):
    mails = models.Mail.objects.all()  # 在主页面中显示的快递
    return render(request, 'index.html', {'mails': mails})  # 返回字典

@login_required
def mailpage(request, mail_id):
    mail = models.Mail.objects.get(pk=mail_id)
    if mail.WhereUP == '12':
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
    return render(request,'user.html')

@login_required
def take(request,mail_id):
    mail = models.Mail.objects.get(pk=mail_id)
    mail.delete()
    return HttpResponseRedirect('http://127.0.0.1:8000')


