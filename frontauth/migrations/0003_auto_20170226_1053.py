# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-26 02:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontauth', '0002_frontuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frontuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='frontauth.FrontUserModel'),
        ),
    ]
