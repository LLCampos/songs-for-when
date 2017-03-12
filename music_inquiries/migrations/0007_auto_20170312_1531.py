# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-12 15:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('music_inquiries', '0006_auto_20170311_1739'),
    ]

    operations = [
        migrations.CreateModel(
            name='SuggestionVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modality', models.CharField(choices=[('positive', 'positive'), ('negative', 'negative')], max_length=8)),
                ('suggestion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music_inquiries.SongSuggestion')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='suggestionvote',
            unique_together=set([('user', 'suggestion')]),
        ),
    ]
