# Generated by Django 3.0.2 on 2020-01-15 06:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0004_boardinvite_disable'),
    ]

    operations = [
        migrations.RenameField(
            model_name='boardinvite',
            old_name='member',
            new_name='member_email',
        ),
    ]
