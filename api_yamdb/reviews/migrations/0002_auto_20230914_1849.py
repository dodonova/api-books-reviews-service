# Generated by Django 3.2 on 2023-09-14 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='genres',
            field=models.ManyToManyField(to='reviews.Genre'),
        ),
        migrations.DeleteModel(
            name='Genre_Title',
        ),
    ]
