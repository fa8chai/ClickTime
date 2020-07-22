from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from profile.models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

    
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    
    list_display = ('email', 'first_name','last_name','is_staff', 'is_active',)
    list_filter = ('email', 'first_name','last_name', 'is_staff', 'is_active',)
    
    fieldsets = (
        (None, {'fields': ('email' ,'password')}),
        ('Personal info', {'fields': ('first_name','last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_superuser')}),
        ('Important dates', {'fields':('last_login','date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name','last_name','email' ,'password1', 'password2', 'is_staff', 'is_active','is_superuser')}
        ),
    )
    search_fields = ('email','first_name', 'last_name')
    ordering = ('email',)
    inlines = (ProfileInline, )

   


admin.site.register(CustomUser, CustomUserAdmin)