# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-06 00:28
from __future__ import unicode_literals

import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('text', models.TextField(help_text='Edit in Markdown')),
                ('text_rendered', models.TextField(editable=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'created',
                'db_table': 'answers',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('text', models.CharField(max_length=512)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='text', unique=True)),
                ('signature', models.CharField(editable=False, max_length=28, unique=True)),
                ('details', models.TextField(blank=True, default=None, help_text='Edit in Markdown', null=True)),
                ('details_rendered', models.TextField(blank=True, default=None, editable=False, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to=settings.AUTH_USER_MODEL)),
                ('related', models.ManyToManyField(related_name='_question_related_+', to='fugato.Question')),
            ],
            options={
                'get_latest_by': 'created',
                'db_table': 'questions',
            },
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='fugato.Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='related',
            field=models.ManyToManyField(related_name='_answer_related_+', to='fugato.Answer'),
        ),
    ]