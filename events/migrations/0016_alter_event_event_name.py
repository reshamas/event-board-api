# Generated by Django 4.0.3 on 2022-08-24 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_alter_event_organization_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
