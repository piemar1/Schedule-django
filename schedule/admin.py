from django.contrib import admin
from user_account.models import User
from .models import Person, Team, Schedule




class PersonInLine(admin.TabularInline):
    model = Person
    extra = 3


class TeamAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User', {'fields': ['user']}),
        ('Team Name', {'fields': ['name']}),
    ]
    inlines = [PersonInLine]
    list_display = ('name', 'user')   # dodaje koluny tabeli


class ScheduleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User', {'fields': ['user']}),
        ('Schedule name', {'fields': ['name']}),
        ('Month', {'fields': ['month']}),
        ('Year', {'fields': ['year']}),
        ('Team',{'fields': ['crew']}),
        ('Schedule', {'fields': ['schedule']}),
    ]
    list_display = ('name', 'user', 'crew', 'month', 'year')   # dodaje koluny tabeli
    list_filter = ['user']
    search_fields = ['name', 'month', 'year']



admin.site.register(Team, TeamAdmin)
admin.site.register(Schedule, ScheduleAdmin)


