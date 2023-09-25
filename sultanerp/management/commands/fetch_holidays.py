from django.core.management.base import BaseCommand
from ...models import PublicHoliday
from ...views import get_public_holidays

# How to create custom django-admin commands
# "https://docs.djangoproject.com/en/4.2/howto/custom-management-commands/#module-django.core.management"

# run this command in the terminal: python manage.py fetch_holidays 2023 for the next 3 years (2023, 2024, 2025)
# and python manage.py fetch_holidays 2024 
# (for 2025)

class Command(BaseCommand):
    help = 'Fetch public holidays from the API and store them in the database'

    def add_arguments(self, parser):
        parser.add_argument(
            'year', type=int, help='Year for which the holidays should be fetched')

    def handle(self, *args, **kwargs):
        year = kwargs['year']
        holidays = get_public_holidays(year)

        for holiday in holidays:
            if not PublicHoliday.objects.filter(date=holiday['date']).exists():
                PublicHoliday.objects.create(
                    date=holiday['date'], name=holiday['title'])

        self.stdout.write(self.style.SUCCESS(
            f"Succes: added public holidays for the year {year}"))

