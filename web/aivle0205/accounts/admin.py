from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,AuthSms

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('phone','birthdate', 'address')}),
    )
    list_display = ('phone','username', 'birthdate', 'address', 'date_joined', 'email')

admin.site.register(User, CustomUserAdmin)

admin.site.register(AuthSms)