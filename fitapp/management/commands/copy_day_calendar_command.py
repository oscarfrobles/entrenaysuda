from django.core.management.base import BaseCommand
from fitapp.operaciones import checkCalendarToday

class Command(BaseCommand):


    def handle(self, *args, **kwargs):
        checkCalendarToday()