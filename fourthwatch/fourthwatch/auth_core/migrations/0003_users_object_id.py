# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-07-20 15:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_core', '0002_auto_20180720_2121'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='object_id',
            field=models.PositiveIntegerField(default=None),
            preserve_default=False,
        ),
    ]