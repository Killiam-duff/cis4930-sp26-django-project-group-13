import json

import pandas as pd
from django.core.paginator import Paginator
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
    #  BATTING DATA
    batting_qs = BattingRecord.objects.select_related('team').values(
        'player', 'batting_avg', 'ops', 'home_runs', 'war',
        'team__league', 'team__abbreviation',
    )
    batting_df = pd.DataFrame(list(batting_qs))

    batting_chart_ops_league = {}      # bar  – avg OPS by league
    batting_chart_top_ops = {}         # bar  – top 10 players by OPS
    batting_chart_ops_dist = {}        # doughnut – OPS tier distribution
    batting_summary = {}
    league_stats_rows = []

    if not batting_df.empty:
        # Aggregation 1: avg OPS / HR / WAR by league (bar chart)
        league_grp = batting_df.groupby('team__league').agg(
            avg_ops=('ops', 'mean'),
            avg_hr=('home_runs', 'mean'),
            avg_war=('war', 'mean'),
        ).reset_index()

        batting_chart_ops_league = {
            'labels': league_grp['team__league'].tolist(),
            'ops':    [round(v, 3) for v in league_grp['avg_ops'].tolist()],
            'hr':     [round(v, 1) for v in league_grp['avg_hr'].tolist()],
            'war':    [round(v, 2) for v in league_grp['avg_war'].tolist()],
        }

        # Aggregation 2: top 10 players by OPS (horizontal bar chart)
        top10 = batting_df.nlargest(10, 'ops')[['player', 'ops', 'team__abbreviation']]
        batting_chart_top_ops = {
            'labels': [f"{r['player']} ({r['team__abbreviation']})" for _, r in top10.iterrows()],
            'ops':    [round(v, 3) for v in top10['ops'].tolist()],
        }

        # Aggregation 3: OPS tier distribution (doughnut chart)
        def ops_tier(val):
            if val >= 0.900:   return 'Elite (≥.900)'
            elif val >= 0.800: return 'Great (.800–.899)'
            elif val >= 0.700: return 'Average (.700–.799)'
            else:              return 'Below avg (<.700)'

        tier_order = ['Elite (≥.900)', 'Great (.800–.899)', 'Average (.700–.799)', 'Below avg (<.700)']
        batting_df['ops_tier'] = batting_df['ops'].apply(ops_tier)
        tier_counts = batting_df['ops_tier'].value_counts().reindex(tier_order, fill_value=0)
        batting_chart_ops_dist = {
            'labels': tier_order,
            'counts': tier_counts.tolist(),
        }

        # Summary stats for batting
        batting_summary = {
            'total_players': len(batting_df),
            'avg_batting_avg': round(batting_df['batting_avg'].mean(), 3),
            'avg_ops':         round(batting_df['ops'].mean(), 3),
            'max_ops':         round(batting_df['ops'].max(), 3),
            'min_ops':         round(batting_df['ops'].min(), 3),
            'avg_hr':          round(batting_df['home_runs'].mean(), 1),
            'max_hr':          int(batting_df['home_runs'].max()),
            'avg_war':         round(batting_df['war'].mean(), 2),
            'max_war':         round(batting_df['war'].max(), 2),
        }

        # Table rows: league breakdown
        league_stats_rows = league_grp.rename(columns={
            'team__league': 'league',
            'avg_ops': 'avg_ops',
            'avg_hr': 'avg_hr',
            'avg_war': 'avg_war',
        }).to_dict(orient='records')
        for row in league_stats_rows:
            row['avg_ops'] = round(row['avg_ops'], 3)
            row['avg_hr']  = round(row['avg_hr'], 1)
            row['avg_war'] = round(row['avg_war'], 2)

    #  WEATHER DATA
    weather_qs = WeatherRecord.objects.select_related('city').values(
        'date', 'temp_max_f', 'temp_min_f', 'precipitation_in',
        'windspeed_max_mph', 'city__name',
    ).order_by('city__name', 'date')
    weather_df = pd.DataFrame(list(weather_qs))

    weather_chart_temp = {}        # line – avg max temp by month per city
    weather_chart_precip = {}      # bar – total precipitation by city
    weather_summary = {}
    city_stats_rows = []

    if not weather_df.empty:
        weather_df['date'] = pd.to_datetime(weather_df['date'])
        weather_df['month'] = weather_df['date'].dt.to_period('M').astype(str)

        # Aggregation 4: avg max temp by month, per city (line chart)
        cities = sorted(weather_df['city__name'].unique().tolist())
        months = sorted(weather_df['month'].unique().tolist())
        month_city = weather_df.groupby(['month', 'city__name'])['temp_max_f'].mean().round(1)

        datasets_temp = []
        palette = ['#0d6efd', '#dc3545', '#198754', '#fd7e14', '#6f42c1']
        for i, city in enumerate(cities):
            vals = [
                round(month_city.get((m, city), None) or 0, 1)
                for m in months
            ]
            datasets_temp.append({
                'label': city,
                'data': vals,
                'borderColor': palette[i % len(palette)],
                'backgroundColor': palette[i % len(palette)] + '22',
                'tension': 0.3,
                'fill': False,
            })
        weather_chart_temp = {'labels': months, 'datasets': datasets_temp}

        # Aggregation 5: total precipitation by city (bar chart)
        precip_by_city = weather_df.groupby('city__name')['precipitation_in'].sum().round(2)
        weather_chart_precip = {
            'labels': precip_by_city.index.tolist(),
            'values': precip_by_city.values.tolist(),
        }

        # Summary stats for weather
        weather_summary = {
            'total_records': len(weather_df),
            'avg_max_temp':  round(weather_df['temp_max_f'].mean(), 1),
            'avg_min_temp':  round(weather_df['temp_min_f'].mean(), 1),
            'max_temp':      round(weather_df['temp_max_f'].max(), 1),
            'min_temp':      round(weather_df['temp_min_f'].min(), 1),
            'avg_precip':    round(weather_df['precipitation_in'].mean(), 2),
        }

        # Table rows: city breakdown
        city_grp = weather_df.groupby('city__name').agg(
            temp_max_f=('temp_max_f', 'mean'),
            temp_min_f=('temp_min_f', 'mean'),
            precipitation_in=('precipitation_in', 'mean'),
            windspeed_max_mph=('windspeed_max_mph', 'mean'),
        ).reset_index().rename(columns={'city__name': 'city__name'})
        city_stats_rows = city_grp.round(2).to_dict(orient='records')

    return render(request, 'myapp/analytics.html', {
        # flags
        'batting_df_empty': batting_df.empty,
        'weather_df_empty': weather_df.empty,
        # batting charts (json-safe)
        'batting_chart_ops_league_json': json.dumps(batting_chart_ops_league),
        'batting_chart_top_ops_json':    json.dumps(batting_chart_top_ops),
        'batting_chart_ops_dist_json':   json.dumps(batting_chart_ops_dist),
        # batting table / summary
        'batting_summary':    batting_summary,
        'league_stats_rows':  league_stats_rows,
        # weather charts (json-safe)
        'weather_chart_temp_json':   json.dumps(weather_chart_temp),
        'weather_chart_precip_json': json.dumps(weather_chart_precip),
        # weather table / summary
        'weather_summary':  weather_summary,
        'city_stats_rows':  city_stats_rows,
    })
