import http.client
from urllib import parse

from django.contrib.auth.decorators import login_required,permission_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.utils import timezone

from . import models
from .forms import MailForm, CaptchaTestForm,CheckForm
from .check import send_sms,createPhoneCode
import qiniu

key = "7720028ac388fe8b413e2cd91a532307" # 云片网个人秘钥
text = "【航宇青协】您的”帮我跑跑“平台验证码是" # 云片网模板语言

# apikey:成功注册后登录云片官网,进入后台可查看
# text:需要使用已审核通过的模板或者默认模板
# mobile:接收的手机号,仅支持单号码发送

# def register(request):
# 	if request.method == 'GET':
# 		rf = RegisterForm()
# 		return render(request, 'register.html', {'form': rf})
# 	if request.method == 'POST':
# 		rf = RegisterForm(request.POST)
# 		if request.POST.get('raw_username', '') != '':  # 不懂
# 			try:
# 				user = models.NewUser.objects.get(username=request.POST.get('raw_username', ''))
# 			except ObjectDoesNotExist:
# 				return render(request, 'register.html', {'form': rf, 'msg': "该用户名可用！"})
# 			else:
# 				return render(request, 'register.html', {'form': rf, 'msg': "该用户名已存在！"})
# 		else:
# 			if rf.is_valid():
# 				username = rf.cleaned_data['username']
# 				# userID = rf.cleaned_data['userID']    #尝试测试学号
# 				filter_result1 = models.NewUser.objects.filter(username=username)
# 				# filter_result2 = models.NewUser.objects.filter(userID=userID)
# 				if len(filter_result1) > 0:  # 用户名(手机号码）或 学号 重名
# 					return render(request, 'register.html', {'form': rf, 'msg': "该手机号或学号已存在！"})
# 				else:
# 					username = rf.cleaned_data['username']
# 					userID = rf.cleaned_data['userID']
# 					password1 = rf.cleaned_data['password1']
# 					password2 = rf.cleaned_data['password2']
# 				if password1 != password2:
# 					return render(request, 'register.html', {'form': rf, 'msg': "输入密码不一致！"})
# 				else:
# 					user = models.NewUser(username=username, password=password1)
# 					user.set_password(password1)  # 重要！！！设置密码加密，不然是明文，admin里密码显示也是明文，登录不了
# 					user.save()
# 					new_password = password1.encode('ascii')
# 					u = models.UserProfile.objects.create(user=user, username=username,
# 					                                      userID=userID, password=new_password,
# 					                                      userphone=username)  # 注册成功则创建对应user profile
# 					u.save()
# 					return redirect('/login', {'form': rf, 's': "注册成功！请登录！"})
# 			else:
# # 				return render(request, 'register.html', {'form': rf, 'msg': "等待正确输入！"})
def register(request):
    msg = ""
    if request.POST:
        rf = CaptchaTestForm(request.POST)
        if rf.is_valid():
            username = rf.cleaned_data['username']
            filter_result1 = models.NewUser.objects.filter(username=username)
            if len(filter_result1) > 0:
                msg = "该手机或学号已经存在"
                return render(request, 'register.html', {'rf': rf, 'msg': msg})
            else:
                userID = rf.cleaned_data['userID']  #学号
                password1 = rf.cleaned_data['password1'] #密码
                checknum = createPhoneCode()    #生成的验证码

            user = models.NewUser(username=username, password=password1)
            user.set_password(password1)  # 重要！！！设置密码加密，不然是明文，admin里密码显示也是明文，登录不了
            user.save()
            new_password = password1.encode('ascii')
            u = models.UserProfile.objects.create(user=user, username=username,
                                                  userID=userID, password=new_password,
                                                  userphone=username,checknum=checknum)  # 注册成功则创建对应user

            u.save()
            sms_log = send_sms(key,text+checknum,username)
            print(sms_log)
            return redirect('/login', {'rf': rf, 's': "注册成功！请登录！"})

        else:
            # return HttpResponse('么么哒！验证码是小写哟')
            msg = "你的验证码输入有误"
    else:
        rf = CaptchaTestForm()
    return render(request, 'register.html', {'rf': rf, 'msg': msg})


@login_required
def index(request):
    all_mails = models.Mail.objects.all()  # 在主页面中显示的快递
    mail = []
    for x in all_mails:
        if x.Situation == 0:  # 只显示没有被取的快递
            mail.append(x)

    return render(request, 'index.html', {'mails': mail})  # 返回字典


@permission_required('main.success_check',login_url='/user') #  转义到check
def mailpage(request, mail_id):
    mail = models.Mail.objects.get(pk=mail_id)
    return render(request, 'mailpage.html', {'mail': mail})


@login_required
def Mail(request):
    if request.method == 'POST':
        qf = MailForm(request.POST)
        if qf.is_valid():
            user = request.user
            whereup = qf.cleaned_data['whereup']
            wheredown = qf.cleaned_data['wheredown']
            detail = qf.cleaned_data['detail']
            models.Mail.objects.create(WhereUP=whereup, WhereDown=wheredown, Host_user=user, Detail=detail)
            u = models.UserProfile.objects.get(user=user)
            u.please_num += 1
            # 请求快递数目+1
            u.save()
            return HttpResponseRedirect('/')
        else:
            p = '快递所在地与到件地都不能为空'
            return render(request, 'new.html', {'form': qf, 'msg': p})

    else:
        return render(request, 'new.html')


@login_required
def user(request):
    user = request.user
    all_mails = models.Mail.objects.all()
    mails = []
    for x in all_mails:
        if x.Take_user == user or x.Host_user == user:
            mails.append(x)
    return render(request, 'user.html', {'mails': mails})


@login_required
def take(request, mail_id):
    user = request.user  # 从当前请求中得到用户名
    mail = models.Mail.objects.get(pk=mail_id)
    if mail.Situation < 1:
        mail.Situation = 1
        mail.Take_user = user  # 这里存在一个问题是如果先前有一个物品已经有了Take_user 则会产生错误！
        mail.Take_time = timezone.now()
        mail.save()
    return HttpResponseRedirect('/user/')


@login_required
def get(request, mail_id):
    mail = models.Mail.objects.get(pk=mail_id)
    mail.Situation = 2  # 到达状态码数
    user = mail.Take_user
    u = models.UserProfile.objects.get(user=user)
    u.do_num += 1
    u.save()
    mail.Receive_time = timezone.now()
    mail.save()
    return HttpResponseRedirect('/user/')


@login_required
def quxiao(request, mail_id):
    models.Mail.objects.get(pk=mail_id).delete()
    user = request.user
    u = models.UserProfile.objects.get(user=user)
    u.please_num -= 1
    u.kind_num -= 5  # 信誉度扣除5分
    u.save()
    return HttpResponseRedirect('/user/')

@login_required
def check(request):
    user = request.user
    u = models.UserProfile.objects.get(user=user)
    if request.method == 'POST':
        form = CheckForm(request.POST,request.FILES)
        if form.is_valid():
            u.myimage = form.cleaned_data['updatephoto']
            u.save()
        return HttpResponse("success! boy!")
    else:
        form = CheckForm()
    return render(request,'check.html',{'form':form})