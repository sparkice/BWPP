from django.contrib import admin
from .models import Mail, NewUser, UserProfile


# Register your models here.

class MailAdmin(admin.ModelAdmin):
    list_display = ('id', 'Host_user', 'Take_user','WhereUP', 'WhereDown', 'Situation', 'Push_time', 'Take_time', 'Receive_time','Detail')


class NewUserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','myname','username', 'userID', 'kind_num','please_num','do_num','checknum','zhiyuan','situation','myimage')

# class NewUserAdmin(admin.ModelAdmin):
#     list_display = ('user','permissions')
admin.site.register(Mail, MailAdmin)
admin.site.register(NewUser)
admin.site.register(UserProfile,NewUserProfileAdmin)
