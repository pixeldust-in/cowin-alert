# Generated by Django 3.2 on 2021-05-01 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cowincenter',
            name='block_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='cowincenter',
            name='district_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='cowincenter',
            name='state_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
