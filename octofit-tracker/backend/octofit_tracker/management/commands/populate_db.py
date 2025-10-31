from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Deleting old data...')
        Activity.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()
        Workout.objects.all().delete()
        Leaderboard.objects.all().delete()

        self.stdout.write('Creating teams...')
        marvel = Team.objects.create(name='Marvel', description='Marvel superheroes')
        dc = Team.objects.create(name='DC', description='DC superheroes')

        self.stdout.write('Creating users...')
        users = [
            User.objects.create(email='tony@marvel.com', name='Tony Stark', team=marvel),
            User.objects.create(email='steve@marvel.com', name='Steve Rogers', team=marvel),
            User.objects.create(email='bruce@marvel.com', name='Bruce Banner', team=marvel),
            User.objects.create(email='clark@dc.com', name='Clark Kent', team=dc),
            User.objects.create(email='bruce@dc.com', name='Bruce Wayne', team=dc),
            User.objects.create(email='diana@dc.com', name='Diana Prince', team=dc),
        ]

        self.stdout.write('Creating activities...')
        for user in users:
            Activity.objects.create(user=user, type='Running', duration=30, date=timezone.now().date())
            Activity.objects.create(user=user, type='Cycling', duration=45, date=timezone.now().date())

        self.stdout.write('Creating workouts...')
        w1 = Workout.objects.create(name='Super Strength', description='Strength workout')
        w2 = Workout.objects.create(name='Flight Training', description='Flight workout')
        w1.suggested_for.set([marvel, dc])
        w2.suggested_for.set([dc])

        self.stdout.write('Creating leaderboards...')
        Leaderboard.objects.create(team=marvel, points=100)
        Leaderboard.objects.create(team=dc, points=120)

        self.stdout.write('Ensuring unique index on user email...')
        client = MongoClient('mongodb://localhost:27017')
        db = client['octofit_db']
        db.user.create_index('email', unique=True)
        self.stdout.write(self.style.SUCCESS('Database populated with test data!'))
