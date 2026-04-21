from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# stores team info from the csv
class Team(models.Model):
    LEAGUE_CHOICES = [
        ('AL', 'American League'),
        ('NL', 'National League'),
        ('2LG', 'Both Leagues'),  # players who played on two teams that season
    ]
    abbreviation = models.CharField(max_length=5, unique=True)
    league = models.CharField(max_length=3, choices=LEAGUE_CHOICES)

    def __str__(self):
        return self.abbreviation

    class Meta:
        ordering = ['abbreviation']


class BattingRecord(models.Model):
    SOURCE_CHOICES = [('csv', 'CSV Import'), ('api', 'API Fetch')]

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='batting_records')
    player = models.CharField(max_length=100)
    age = models.IntegerField(validators=[MinValueValidator(18), MaxValueValidator(50)])  # keeps bad csv data out
    war = models.FloatField()
    games = models.IntegerField()
    plate_appearances = models.IntegerField()
    at_bats = models.IntegerField()
    runs = models.IntegerField()
    hits = models.IntegerField()
    doubles = models.IntegerField()
    triples = models.IntegerField()
    home_runs = models.IntegerField()
    rbi = models.IntegerField()
    stolen_bases = models.IntegerField()
    caught_stealing = models.IntegerField()
    walks = models.IntegerField()
    strikeouts = models.IntegerField()
    batting_avg = models.FloatField()
    obp = models.FloatField()
    slg = models.FloatField()
    ops = models.FloatField()
    ops_plus = models.IntegerField()
    hbp = models.IntegerField()
    source = models.CharField(max_length=3, choices=SOURCE_CHOICES, default='csv')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player} ({self.team})"

    class Meta:
        ordering = ['-ops']
        # not a perfect unique key but a player shouldnt appear at the same age for the same team twice
        unique_together = ['player', 'team', 'age']


class City(models.Model):
    # used for the open meteo api cities
    name = models.CharField(max_length=100, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'cities'


class WeatherRecord(models.Model):
    SOURCE_CHOICES = [('csv', 'CSV Import'), ('api', 'API Fetch')]

    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='weather_records')
    date = models.DateField()
    temp_max_f = models.FloatField(null=True, blank=True)
    temp_min_f = models.FloatField(null=True, blank=True)
    precipitation_in = models.FloatField(null=True, blank=True)
    windspeed_max_mph = models.FloatField(null=True, blank=True)
    source = models.CharField(max_length=3, choices=SOURCE_CHOICES, default='api')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city} - {self.date}"

    class Meta:
        ordering = ['-date']
        unique_together = ['city', 'date']
