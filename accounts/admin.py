from django.contrib import admin
from django.contrib.auth.admin import UserAdmin #for secure that password of user cant be changed in database
from django.utils.html import format_html
from .models import Account,UserProfile



#the classes in admin is created to perform operation on the table which is created in database vai model.py classes hence the name of models class is merged with Admin
class AccountAdmin(UserAdmin): #field we want to display in Accounts table in database
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active') #field we want to display in users table
    list_display_links = ('email', 'first_name', 'last_name') #on which parameters we want to apply link
    readonly_fields = ('last_login', 'date_joined') #readonly fields
    ordering = ('-date_joined',) #- shows in decending order 

    filter_horizontal = ()
    list_filter = ()
    fieldsets = () #will make password readonly

class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object): #for user image
        return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_picture.url))
    thumbnail.short_description = 'Profile Picture'
    list_display = ('thumbnail', 'user', 'city', 'state', 'country')

# Register your models here.
admin.site.register(Account,AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
