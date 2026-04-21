from django.contrib import admin

from .models import BattingRecord, City, Team, WeatherRecord


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['abbreviation', 'league']
    list_filter = ['league']
    search_fields = ['abbreviation']


@admin.register(BattingRecord)
class BattingRecordAdmin(admin.ModelAdmin):
    list_display = ['player', 'team', 'age', 'batting_avg', 'ops', 'home_runs', 'war', 'source']
    list_filter = ['team__league', 'source']
    search_fields = ['player', 'team__abbreviation']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'latitude', 'longitude']
    search_fields = ['name']


@admin.register(WeatherRecord)
class WeatherRecordAdmin(admin.ModelAdmin):
    list_display = ['city', 'date', 'temp_max_f', 'temp_min_f', 'precipitation_in', 'source']
    list_filter = ['city', 'source']
    search_fields = ['city__name']
