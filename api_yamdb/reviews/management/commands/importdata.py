import csv, sqlite3
# from pathlib import Path
# from os import subprocess
import subprocess
import os
from pathlib import Path

from django.core.management.base import BaseCommand

from reviews.models import (
    Category,
    Genre,
    Title,
    User,
    Review,
    Comment
)

class Command(BaseCommand):
    help = "Import data from csv file to sqlite3 database. By default import all files to db.sqlite3 from static/data/"

    def add_arguments(self, parser):
        parser.add_argument('--db',
                            nargs=1,
                            type=str,
                            required=False,
                            default=None,
                            help='Database file for import.')
        parser.add_argument('--table',
                            nargs=1,
                            type=str,
                            required=False,
                            default=None,
                            help='Table name ib database.')
        parser.add_argument('--csv_file',
                            nargs=1,
                            type=str,
                            required=False,
                            default=None,
                            help='CSV file name with data for import.')
     
    def import_table(self, db, table, csv_file):
        try:   
            if not os.path.isfile(csv_file):
                raise FileExistsError
            result = subprocess.run([
                    'sqlite3',
                    str(db),
                    '-cmd',
                    '.mode csv',
                    f'.import --skip 1 {csv_file} {table}'
                ],
                capture_output=True
            )
        except Exception as err:
            self.stdout.write(self.style.ERROR(
                f'Something wrong with table {table}: {str(err)} \n{csv_file}'))
        else:
            self.stdout.write(self.style.SUCCESS(
                f'Data successfully imported from file {csv_file}.csv to the table {table}.'))


    def handle(self, *args, **options):
        db_name = options['db'][0] if options['db'] is not None else 'db.sqlite3'     
        table_name = options['table'][0] if options['table'] is not None else None
        filename = options['csv_file'][0] if options['csv_file'] is not None else None
        #TODO: почему нужно брать [0] при получении options?
        if filename is None and  table_name is None:   
            model_names = {
                'category': 'reviews_category',
                'genre': 'reviews_genre',
                'title': 'reviews_title',
                'review': 'reviews_review',
                'title_genre': 'reviews_title_genre',
                'comment': 'reviews_comment',
                'user': 'users_user'
            }
            for filename, table_name in model_names.items():
                self.import_table(db_name, table_name, f'static/data/{filename}.csv')
                #TODO: как программно получать путь к папке со статикой?
        else:
            self.import_table(db_name, table_name, filename)
            
        self.stdout.write(self.style.SUCCESS('Command importdata done.'))