from django.contrib import admin
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
    list_display = ('name', 'user')


class ScheduleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User', {'fields': ['user']}),
        ('Schedule name', {'fields': ['name']}),
        ('Month', {'fields': ['month']}),
        ('Year', {'fields': ['year']}),
        ('Team', {'fields': ['crew']}),
    ]
    list_display = ('name', 'user', 'crew', 'month', 'year')
    list_filter = ['user']
    search_fields = ['name', 'month', 'year']


admin.site.register(Team, TeamAdmin)
admin.site.register(Schedule, ScheduleAdmin)
