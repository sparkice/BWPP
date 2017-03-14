from django.contrib import admin
from .models import Mail, NewUser, UserProfile


# Register your models here.

class MailAdmin(admin.ModelAdmin):
    list_display = ('id', 'Host_user', 'Take_user','WhereUP', 'WhereDown', 'Situation', 'Push_time', 'Take_time', 'Receive_time')


class NewUserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'userID', 'kind_num')


admin.site.register(Mail, MailAdmin)
admin.site.register(NewUser)
admin.site.register(UserProfile)
