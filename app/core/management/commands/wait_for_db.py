from time import sleep

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    """
    Django command to pause execution until database is avaliable
    """

    def handle(self, *args, **options):
        self.stdout.write("Waiting for database...")

        db_connection = None

        while not db_connection:
            try:
                db_connection = connections["default"]
            except OperationalError:
                self.stdout.write("Database unavaliable, waiting 1 second...")
                sleep(1)

        self.stdout.write(self.style.SUCCESS("Database avaliable!"))
