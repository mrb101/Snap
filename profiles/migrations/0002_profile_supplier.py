# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-12 07:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='supplier',
            field=models.BooleanField(default=False),
        ),
    ]
