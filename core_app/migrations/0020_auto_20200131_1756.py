# Generated by Django 3.0.2 on 2020-01-31 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0019_auto_20200131_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='title',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
