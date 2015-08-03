# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20150725_2119'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizer',
            name='has_permission_to_create_category',
            field=models.BooleanField(default=False),
        ),
    ]
