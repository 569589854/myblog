# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-01-14 08:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_auto_20170114_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlemodel',
            name='public_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
