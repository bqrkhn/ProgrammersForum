# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-07 19:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20170727_1933'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-datetime']},
        ),
    ]
