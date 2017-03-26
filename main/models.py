from django.contrib.auth.models import User, AbstractUser
from django.db import models


# Create your models here.
# 代替系统默认的用户系统
class NewUser(AbstractUser):
    profile = models.CharField('profile', default='', max_length=256)
    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '个人关键'
        verbose_name_plural = '个人关键'


class UserProfile(models.Model):
    """This function Links UserProfile to a User model instance."""
    user = models.OneToOneField(NewUser, unique=True, verbose_name='用户额外信息')
    username = models.CharField(max_length=11)  # 个人账户名（也就是手机号码）
    userphone = models.CharField(max_length=12)  # 手机号码
    userID = models.CharField(max_length=10)  # 学号
    # 第三次增加！
    myname = models.CharField(max_length=10)  # 个人姓名
    checknum = models.IntegerField()  # 个人验证码
    zhiyuan = models.IntegerField(default=0)  # 志愿服务时长
    situation = models.IntegerField(default=0)  # 所处环境，0表示注册好了，1表示1正在审核，2表示审核通过，-1表示封号
    myimage = models.ImageField(max_length=100,blank=True,upload_to='upload/%Y/%m/%d') #　个人照片哼唧
    # ！
    password = models.CharField(max_length=20)  # 密码
    please_num = models.IntegerField(default=0)  # 委托快递数量
    do_num = models.IntegerField(default=0)  # 完成快递数量
    star_num = models.IntegerField(default=0)  # 被点赞数
    kind_num = models.IntegerField(default=60)  # 友善度



    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = '个人详情'
        verbose_name_plural = '个人详情'


class Mail(models.Model):
    """Imformation about kuai di"""
    WhereUP = models.CharField(max_length=10)  # 存储快递网点信息
    WhereDown = models.CharField(max_length=10)  # 存储快递接受地点
    Detail = models.CharField(max_length=100, null=True,blank=True)  # 更多细节填充,可以为空
    Push_time = models.DateTimeField(auto_now_add=True)  # 存储发送时间
    Take_time = models.DateTimeField(auto_now_add=False, null=True,blank=True)  # 拿取快递时间
    Receive_time = models.DateTimeField(auto_now_add=False, null=True,blank=True)  # 收到快递时间
    Host_user = models.ForeignKey('NewUser', blank=True)  # 快递所有者信息
    Take_user = models.ForeignKey('NewUser', blank=True, related_name='+', null=True)  # 送快递人的信息
    Situation = models.IntegerField(default=0)  # 当前快递状态 0 表示没有人接收 1 表示有人接收还没有送到 2表示已经送到 -1表示取消

    class Meta:
        verbose_name = '快递'
        verbose_name_plural = '快递'
        ordering = ['-Push_time']  # 按时间下降排序


class Task(models.Model):
    class Meta:
        permissions = (
            ("success_check", "Can do all thing"),
            ("check_ing", "Can only publish kuai di"),
        )
