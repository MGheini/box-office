# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_auto_20150721_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_date',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_deadline',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_description',
            field=models.TextField(blank=True),
        ),
    ]
