# Generated by Django 3.2 on 2021-05-03 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_remove_alertrequest_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cowinsession',
            name='available_capacity',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
