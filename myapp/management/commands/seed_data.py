import csv
from pathlib import Path

from django.core.management.base import BaseCommand

from myapp.models import BattingRecord, Team

# path goes up 4 levels from this file to reach project root
CSV_PATH = Path(__file__).resolve().parent.parent.parent.parent / 'data' / 'raw' / 'batting_stats.csv'


class Command(BaseCommand):
    help = 'Load batting stats CSV into the database'

    def handle(self, *args, **options):
        created = 0
        skipped = 0

        # utf-8-sig strips the BOM character at the start of the file
        with open(CSV_PATH, newline='', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                team, _ = Team.objects.get_or_create(
                    abbreviation=row['Team'],
                    defaults={'league': row['Lg'] if row['Lg'] in ('AL', 'NL', '2LG') else 'AL'},
                )
                _, was_created = BattingRecord.objects.get_or_create(
                    player=row['Player'],
                    team=team,
                    age=int(row['Age']),
                    defaults={
                        'war': float(row['WAR']),
                        'games': int(row['G']),
                        'plate_appearances': int(row['PA']),
                        'at_bats': int(row['AB']),
                        'runs': int(row['R']),
                        'hits': int(row['H']),
                        'doubles': int(row['2B']),
                        'triples': int(row['3B']),
                        'home_runs': int(row['HR']),
                        'rbi': int(row['RBI']),
                        'stolen_bases': int(row['SB']),
                        'caught_stealing': int(row['CS']),
                        'walks': int(row['BB']),
                        'strikeouts': int(row['SO']),
                        'batting_avg': float(row['BA']),
                        'obp': float(row['OBP']),
                        'slg': float(row['SLG']),
                        'ops': float(row['OPS']),
                        'ops_plus': int(row['OPS+']),
                        'hbp': int(row['HBP']),
                        'source': 'csv',
                    },
                )
                if was_created:
                    created += 1
                else:
                    skipped += 1

        self.stdout.write(self.style.SUCCESS(
            f'Seeded {created} records, skipped {skipped} duplicates.'
        ))
