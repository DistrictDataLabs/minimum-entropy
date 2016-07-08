# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-07 21:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tagging', '0001_initial'),
        ('fugato', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(related_name='questions', to='tagging.Tag'),
        ),
        migrations.AlterField(
            model_name='question',
            name='related',
            field=models.ManyToManyField(blank=True, related_name='_question_related_+', to='fugato.Question'),
        ),
    ]