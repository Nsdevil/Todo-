# Generated by Django 4.1.5 on 2023-01-03 06:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lead', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lead',
            old_name='starus',
            new_name='status',
        ),
    ]