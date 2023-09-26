import csv
import datetime
import errno
import os
import sqlite3
from pathlib import Path

from api_yamdb.settings import (
    DATABASES,
    STATICFILES_DIRS
)
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Provides importing data from csv files to sqlite database.

    Command imortdata takes csv files from folder static/data/
    and import data to the relevant tables ib database db.sqlite3.

    """

    CSV_MODELS = {
        'category': 'reviews_category',
        'genre': 'reviews_genre',
        'title': 'reviews_title',
        'review': 'reviews_review',
        'title_genre': 'reviews_genretitle',
        'comment': 'reviews_comment',
        'user': 'users_user'
    }

    DEFAULT_DB = Path(DATABASES["default"]["NAME"])
    CSV_FOLDER = Path(STATICFILES_DIRS[0] / "data")

    help = (
        f'Import data from csv file to sqlite3 database. '
        f'Import csv files to {DEFAULT_DB} from {CSV_FOLDER}'
    )

    def handle(self, *args, **options):
        """Import data from csv files to sqlite3 database."""

        db_name = self.DEFAULT_DB

        model_names = self.CSV_MODELS
        for filename, table_name in model_names.items():
            full_filename = f'{self.CSV_FOLDER}/{filename}.csv'
            self.stdout.write(
                f'Importing to {db_name}, {table_name} from {full_filename}'
            )
            try:
                self.check_db_csv(db_name, full_filename)
                import_method = getattr(self, f'import_{filename}')
                conn = sqlite3.connect(db_name)
                cursor = conn.cursor()
                import_method(cursor, full_filename, self.CSV_MODELS[filename])
            except Exception as err:
                err_msg = (
                    f'Error import from {full_filename} to the table '
                    f'{table_name}.\n{err}'
                )
                self.stdout.write(
                    self.style.ERROR(err_msg)
                )
            else:
                conn.commit()
                conn.close()
                success_msg = (
                    f'Data imported from {full_filename} '
                    f'to the table {table_name}.'
                )
                self.stdout.write(
                    self.style.SUCCESS(success_msg)
                )

    def check_db_csv(self, db, csv_file):
        if not os.path.isfile(csv_file):
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), csv_file
            )
        if not os.path.isfile(db):
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), db
            )
        return True

    def import_category(self, cursor, csv_file, table):
        with open(csv_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            query = (
                f'INSERT INTO {table} '
                f'(id, slug, name) '
                f'VALUES (?, ?, ?)'
            )
            for row in reader:
                cursor.execute(
                    query, (
                        row['id'],
                        row['slug'],
                        row['name'],
                    )
                )

    def import_genre(self, cursor, csv_file, table):
        self.import_category(cursor, csv_file, table)

    def import_title(self, cursor, csv_file, table):
        with open(csv_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            query = (
                f'INSERT INTO {table} '
                f'(id, name, year, description, category_id) '
                f'VALUES (?, ?, ?, ?, ?)'
            )
            for row in reader:
                cursor.execute(
                    query, (
                        row['id'],
                        row['name'],
                        row['year'],
                        "Нет описания",
                        row['category'],
                    )
                )

    def import_title_genre(self, cursor, csv_file, table):
        with open(csv_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            query = (
                f'INSERT INTO {table} '
                f'(id, genre_id, title_id) '
                f'VALUES (?, ?, ?)'
            )
            for row in reader:
                cursor.execute(
                    query, (
                        row['id'],
                        row['genre_id'],
                        row['title_id'],
                    )
                )

    def import_review(self, cursor, csv_file, table):
        with open(csv_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            query = (
                f'INSERT INTO {table} '
                f'(id, text, score, pub_date, author_id, title_id) '
                f'VALUES (?, ?, ?, ?, ?, ?)'
            )
            for row in reader:
                cursor.execute(
                    query, (
                        row['id'],
                        row['text'],
                        row['score'],
                        row['pub_date'],
                        row['author'],
                        row['title_id']
                    )
                )

    def import_comment(self, cursor, csv_file, table):
        with open(csv_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            query = (
                f'INSERT INTO {table} '
                f'(id, text, pub_date, author_id, review_id) '
                f'VALUES (?, ?, ?, ?, ?)'
            )
            for row in reader:
                cursor.execute(
                    query, (
                        row['id'],
                        row['text'],
                        row['pub_date'],
                        row['author'],
                        row['review_id']
                    )
                )

    def import_user(self, cursor, csv_file, table):
        with open(csv_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            query = (
                f'INSERT INTO {table} '
                f'(id, username, email, role, bio, first_name, last_name, '
                f'password, is_superuser, is_staff, is_active, '
                f'date_joined, confirmation_code) '
                f'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
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
