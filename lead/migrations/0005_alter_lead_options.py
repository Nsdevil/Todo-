# Generated by Django 4.1.5 on 2023-01-06 05:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lead', '0004_lead_team_alter_lead_created_by'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lead',
            options={'ordering': ('name',)},
        ),
    ]