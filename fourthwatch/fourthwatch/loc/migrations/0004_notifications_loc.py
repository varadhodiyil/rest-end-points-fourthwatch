# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-07-23 17:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loc', '0003_notifications'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='loc',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='loc.LOC'),
            preserve_default=False,
        ),
    ]