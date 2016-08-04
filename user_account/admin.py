__author__ = 'Marcin Pieczyński'

from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User Name', {'fields': ['name', 'surname']}),
        ('User Mail', {'fields': ['email']}),
        ('Is User Active', {'fields': ['active']})
    ]
    list_display = ('name', 'surname', 'email', 'active', 'superuser', 'staff')
    list_filter = ['active']

admin.site.register(User, UserAdmin)