from django.contrib import admin
from .models import User,UserProfile
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class CustomUserAdmin(UserAdmin):  #This effectively makes the user details read-only since there are no editable fields visible.
    list_display = ('email','first_name','last_name','username','role','is_active')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(User,CustomUserAdmin)
admin.site.register(UserProfile)