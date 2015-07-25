# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='member',
            options={'verbose_name_plural': 'کاربران نوع مشتری', 'verbose_name': 'کاربر نوع مشتری'},
        ),
        migrations.AlterModelOptions(
            name='organizer',
            options={'verbose_name_plural': 'کاربران نوع برگزارکننده', 'verbose_name': 'کاربر نوع برگزارکننده'},
        ),
    ]
