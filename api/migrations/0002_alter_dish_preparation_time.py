# Generated by Django 3.2.6 on 2021-09-01 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='preparation_time',
            field=models.DurationField(),
        ),
    ]