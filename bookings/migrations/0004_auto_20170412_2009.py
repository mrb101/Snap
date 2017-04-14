# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-12 12:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0003_auto_20170412_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='suppliers', to=settings.AUTH_USER_MODEL),
        ),
    ]
