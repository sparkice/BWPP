from django.db import models
from django.contrib.auth.models import User, AbstractUser


# Create your models here.
# 代替系统默认的用户系统
class NewUser(AbstractUser):
    profile = models.CharField('profile', default='', max_length=256)

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    """This function Links UserProfile to a User model instance."""
    user = models.OneToOneField(NewUser, unique=True, verbose_name='用户额外信息')
    username = models.CharField(max_length=10)  # 个人登录账户名（手机号码）
    userphone = models.CharField(max_length=12)  # 手机号码 ?
    userID = models.CharField(max_length=10)  # 学号
    password = models.CharField(max_length=20)  # 密码
    please_num = models.IntegerField(default=0)  # 委托快递数量
    do_num = models.IntegerField(default=0)  # 完成快递数量
    star_num = models.IntegerField(default=0)  # 被点赞数
    kind_num = models.IntegerField(default=60)  # 友善度

    def __str__(self):
        return self.user.username


class Mail(models.Model):
    """Imformation about kuai di"""
    WhereUP = models.CharField(max_length=10)  # 存储快递网点信息
    WhereDown = models.CharField(max_length=10)  # 存储快递接受地点
    Push_time = models.DateTimeField(auto_now_add=True)  # 存储发送时间
    Take_time = models.DateTimeField(auto_now_add=False)  # 拿取快递时间
    Receive_time = models.DateTimeField(auto_now_add=False)  # 收到快递时间

    Host_user = models.ForeignKey('NewUser', blank=True)  # 快递所有者信息
    Take_user = models.OneToOneField('NewUser', blank=True, related_name='+')  # 送快递人的信息
    Situation = models.IntegerField(default=0)  # 当前快递状态 0 表示没有人接收 1 表示有人接收还没有送到 2表示已经送到

    class Meta:
        ordering = ['-Push_time']  # 按时间下降排序


class Task(models.Model):
    class Meta:
        permissions = (
            ("view_all", "Can see all the infomation"),
            ("close_task", "Can remove a task by setting its status as closed"),
        )
