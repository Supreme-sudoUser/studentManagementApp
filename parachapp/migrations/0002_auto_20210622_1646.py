# Generated by Django 2.2.7 on 2021-06-22 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parachapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='mobile_phone',
            field=models.BigIntegerField(blank=True, default='070', null=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='mobile_phone',
            field=models.BigIntegerField(blank=True, default='070', null=True),
        ),
    ]
