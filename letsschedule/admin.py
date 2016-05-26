from django.contrib import admin
from .models import User, Person, Team, Schedule


class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User Name', {'fields': ['name', 'surname']}),
        ('User Mail', {'fields':['email']}),
        ('Is User Active', {'fields':['active']})
    ]
    list_display = ('name', 'surname', 'email', 'active')   # dodaje koluny tabeli
    list_filter = ['active']

admin.site.register(User, UserAdmin)


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


admin.site.register(Team, TeamAdmin)


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


admin.site.register(Schedule, ScheduleAdmin)






