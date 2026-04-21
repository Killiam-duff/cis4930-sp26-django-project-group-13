import pandas as pd
from django.contrib.admin.views.decorators import staff_member_required
from django.core.management import call_command
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BattingRecordForm
from .models import BattingRecord, WeatherRecord


def home(request):
    total = BattingRecord.objects.count()
    return render(request, 'myapp/home.html', {'total_records': total})


def about(request):
    return render(request, 'myapp/about.html')


def record_list(request):
    records = BattingRecord.objects.select_related('team').all()
    paginator = Paginator(records, 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'myapp/list.html', {'page_obj': page_obj})


def record_detail(request, pk):
    record = get_object_or_404(BattingRecord, pk=pk)
    return render(request, 'myapp/detail.html', {'record': record})


def record_create(request):
    form = BattingRecordForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.source = 'api'
        obj.save()
        return redirect('records')
    return render(request, 'myapp/form.html', {'form': form, 'action': 'Add'})


def record_update(request, pk):
    record = get_object_or_404(BattingRecord, pk=pk)
    form = BattingRecordForm(request.POST or None, instance=record)
    if form.is_valid():
        form.save()
        return redirect('record_detail', pk=pk)
    return render(request, 'myapp/form.html', {'form': form, 'action': 'Edit'})


def record_delete(request, pk):
    record = get_object_or_404(BattingRecord, pk=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('records')
    return render(request, 'myapp/confirm_delete.html', {'record': record})


def analytics(request):
    # batting stats data. from seed_data. BattingRecord model
    # all batting records with team info. Convert to DataFrame for aggregations.
    # TODO: use batting_df to build your charts.
    #   pass results to template as json.dumps
    batting_qs = BattingRecord.objects.select_related('team').values(
        'player', 'batting_avg', 'ops', 'home_runs', 'war',
        'team__league', 'team__abbreviation',
    )
    batting_df = pd.DataFrame(list(batting_qs))

    # weather data. from fetch_data command. WeatherRecord model
    # all fetched weather records with city name. Convert to DataFrame for aggregations.
    # TODO: use weather_df to build our weather charts
    #   run `python manage.py fetch_data` first to populate this table
    weather_qs = WeatherRecord.objects.select_related('city').values(
        'date', 'temp_max_f', 'temp_min_f', 'precipitation_in',
        'windspeed_max_mph', 'city__name',
    ).order_by('city__name', 'date')
    weather_df = pd.DataFrame(list(weather_qs))

    return render(request, 'myapp/analytics.html', {
        # TODO: place real chart data built from the DataFrames above
        'batting_df_empty': batting_df.empty,
        'weather_df_empty': weather_df.empty,
    })

"""
@staff_member_required
def fetch_data_view(request):
    if request.method != 'POST':
        return HttpResponseForbidden()
    call_command('fetch_data')
    return redirect('analytics')
"""
