from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import SignUpForm
from .models import User, Profile

class CustomUserAdmin(UserAdmin):
    add_form = SignUpForm
    model = User
    list_display = ('email', 'username', 'first_name', 'last_name')

admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)