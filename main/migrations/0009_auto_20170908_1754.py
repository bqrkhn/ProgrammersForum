# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-08 12:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20170908_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='codechef_username',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='profile',
            name='hacker_earth_username',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='profile',
            name='hacker_rank_username',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='profile',
            name='spoj_username',
            field=models.CharField(default='', max_length=255),
        ),
    ]