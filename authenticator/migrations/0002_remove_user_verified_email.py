# Generated by Django 4.0 on 2021-12-20 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authenticator', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='verified_email',
        ),
    ]