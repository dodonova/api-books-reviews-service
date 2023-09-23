import subprocess
import os
import csv
import sqlite3
import errno
import datetime
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Provides importing data from csv files to sqlite database.

    By default should start commant "importdata" from the folder
    containing  file manage.py.
    Commant imortdata takes csv files from folder static/data/
    and import data to the relevant tables ib database dd.sqlite3.

    Options --db --table --csv allow to import every table separatly
    from the custom CSV file to the custom database file.
    If you set --table you also must set --csv.
    """
    help = ('Import data from csv file to sqlite3 database. '
            'By default import all files '
            'to db.sqlite3 from static/data/')

    def add_arguments(self, parser):
        parser.add_argument(
            '--db',
            nargs=1,
            type=str,
            required=False,
            default=None,
            help='Database file for import. Dy default import to "db.sqlite3"'
        )
        parser.add_argument(
            '--table',
            nargs=1,
            type=str,
            required=False,
            default=None,
            help='Table name ib database.'
        )
        parser.add_argument(
            '--csv',
            nargs=1,
            type=str,
            required=False,
            default=None,
            help='CSV file name with data for import.'
        )

    def handle(self, *args, **options):
        """Import data from csv files to dsqlite3 database."""
        if options['db'] is not None:
            db_name = options['db'][0]
        else:
            db_name = 'db.sqlite3'
        if options['table'] is not None:
            table_name = options['table'][0]
        else:
            table_name = None
        if options['csv'] is not None:
            filename = options['csv'][0]
        else:
            filename = None
        # TODO: почему нужно брать [0] при получении options?
        if filename is None and table_name is None:
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
                self.stdout.write(
                    f'Importing to {db_name}, {table_name} from {filename}'
                )
                self.import_table(
                    db_name, table_name, f'static/data/{filename}.csv'
                )
        elif filename is None:
            self.stdout.write(self.style.ERROR('CSV filename requiered.'))
        elif table_name is None:
            self.stdout.write(self.style.ERROR('Table name requiered.'))
        else:
            self.import_table(db_name, table_name, filename)

    def import_table(self, db, table, csv_file):
        """Import any table using subprocess except of users_user.

        For importing to the table users_user calls method import_users().
        """
        if not os.path.isfile(csv_file):
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), csv_file
            )
        if not os.path.isfile(db):
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), db
            )
        if table == 'users_user':
            self.import_users(db, csv_file)
        else:
            result = subprocess.run(
                [
                    'sqlite3',
                    str(db),
                    '-cmd',
                    '.mode csv',
                    f'.import --skip 1 {csv_file} {table}'
                ],
                capture_output=True
            )
            if len(result.stdout) > 1:
                self.stdout.write(self.style.SUCCESS(f'{result.stdout}'))
            if len(result.stderr) > 1:
                self.stdout.write(self.style.ERROR(f'{result.stderr}'))

        self.stdout.write(
            self.style.SUCCESS(
                f'Data imported from {csv_file} to the table {table}.'
            )
        )

    def import_users(self, db, csv_file):
        """Import data from user.csv to the table users_user.

        Method fills in missing fields when importing.
        """
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        with open(csv_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            query = (
                'INSERT INTO users_user '
                '(id, username, email, role, bio, first_name, last_name, '
                'password, is_superuser, is_staff, is_active, '
                'date_joined, confirmation_code) '
                'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            )
            for row in reader:
                cursor.execute(
                    query, (
                        row['id'],
                        row['username'],
                        row['email'],
                        row['role'],
                        row['bio'],
                        row['first_name'],
                        row['last_name'],
                        "", 0, 0, 1,
                        datetime.datetime.now(), ""
                    )
                )
        conn.commit()
        conn.close()