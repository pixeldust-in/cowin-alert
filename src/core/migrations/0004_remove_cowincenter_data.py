# Generated by Django 3.2 on 2021-05-01 20:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_cowinsession_session_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cowincenter',
            name='data',
        ),
    ]
