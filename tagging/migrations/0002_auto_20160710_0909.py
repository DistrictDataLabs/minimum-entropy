# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-10 13:09
from __future__ import unicode_literals

import autoslug.fields
from django.db import migrations
from slugify import slugify


class Migration(migrations.Migration):

    dependencies = [
        ('tagging', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='text', slugify=slugify, unique=True),
        ),
    ]