# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-07-24 04:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loc', '0005_auto_20180724_0015'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=10)),
                ('loc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loc.LOC')),
                ('party', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
