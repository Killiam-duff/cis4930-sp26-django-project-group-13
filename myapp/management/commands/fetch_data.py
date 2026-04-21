from datetime import date, timedelta

import requests
from django.core.management.base import BaseCommand
from django.db import transaction

from myapp.models import City, WeatherRecord

BASE_URL = 'https://api.open-meteo.com/v1/forecast'
PAGE_SIZE_DAYS = 7  # forced pagination to meet project requirements -- open meteo api is just too good

CITIES = [
    {'name': 'Tallahassee', 'latitude': 30.4383, 'longitude': -84.2807},
    {'name': 'Pensacola',   'latitude': 30.4213, 'longitude': -87.2169},
    {'name': 'Navarre',     'latitude': 30.4016, 'longitude': -86.8633},
]


# splits a date range into chunks of page_size days (same logic as project 2)
def _build_date_pages(start, end, page_size=PAGE_SIZE_DAYS):
    pages = []
    current = start
    while current <= end:
        page_end = min(current + timedelta(days=page_size - 1), end)
        pages.append((current, page_end))
        current = page_end + timedelta(days=1)
    return pages


class Command(BaseCommand):
    help = 'Fetch weather data from Open-Meteo API for FL cities'

    def add_arguments(self, parser):
        parser.add_argument('--days', type=int, default=90,                     # upgraded to 90 from 14 in prev project to have more data for analytics
                            help='Number of past days to fetch (default: 90)')

    def handle(self, *args, **options):
        end = date.today()
        start = end - timedelta(days=options['days'] - 1)
        pages = _build_date_pages(start, end)
        total_saved = 0

        for city_info in CITIES:
            city, _ = City.objects.get_or_create(
                name=city_info['name'],
                defaults={
                    'latitude': city_info['latitude'],
                    'longitude': city_info['longitude'],
                },
            )
            city_saved = 0

            for page_num, (page_start, page_end) in enumerate(pages, 1):
                self.stdout.write(
                    f"{city_info['name']} page {page_num}/{len(pages)}: "
                    f"{page_start} to {page_end}"
                )
                try:
                    resp = requests.get(
                        BASE_URL,
                        params={
                            'latitude': city_info['latitude'],
                            'longitude': city_info['longitude'],
                            'daily': (
                                'temperature_2m_max,temperature_2m_min,'
                                'precipitation_sum,windspeed_10m_max'
                            ),
                            'start_date': page_start.isoformat(),
                            'end_date': page_end.isoformat(),
                            'temperature_unit': 'fahrenheit',
                            'windspeed_unit': 'mph',
                            'timezone': 'America/New_York',
                        },
                        timeout=10,
                    )
                    resp.raise_for_status()
                    daily = resp.json()['daily']

                    with transaction.atomic():
                        for i, day in enumerate(daily['time']):
                            _, created = WeatherRecord.objects.update_or_create(
                                city=city,
                                date=day,
                                defaults={
                                    'temp_max_f': daily['temperature_2m_max'][i],
                                    'temp_min_f': daily['temperature_2m_min'][i],
                                    'precipitation_in': daily['precipitation_sum'][i],
                                    'windspeed_max_mph': daily['windspeed_10m_max'][i],
                                    'source': 'api',
                                },
                            )
                            if created:
                                city_saved += 1

                except requests.exceptions.RequestException as e:
                    self.stderr.write(
                        f"Error fetching {city_info['name']} page {page_num}: {e}"
                    )

            total_saved += city_saved
            self.stdout.write(f"Saved {city_saved} new records for {city_info['name']}.")

        self.stdout.write(self.style.SUCCESS(f'Done. Total new records: {total_saved}'))
