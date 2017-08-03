from django.core.management.base import BaseCommand, CommandError
from main.models import View
from datetime import datetime, timedelta, timezone


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        views = View.objects.all()
        for view in views:
            if (datetime.now(timezone.utc) - view.time) > timedelta(1):
                view.delete()