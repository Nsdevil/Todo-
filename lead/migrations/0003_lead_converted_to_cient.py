# Generated by Django 4.1.5 on 2023-01-03 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lead', '0002_rename_starus_lead_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='converted_to_cient',
            field=models.BooleanField(default=False),
        ),
    ]
