import csv, sqlite3

from django.core.management.base import BaseCommand, CommandError, CommandParser

from reviews.models import (
    Category,
    Genre,
    Title,
    User,
    Review,
    Comment
)

class Command(BaseCommand):
    help = "Import data from csv file to sqlite3 database."

    def add_arguments(self, parser: CommandParser) -> None:
        # parser.add_argument('filename', nargs='+', type=str)
        # parser.add_argument('tablename', nargs='+', type=str)
        return super().add_arguments(parser)
    
    def handle(self, *args, **options):
        pass
