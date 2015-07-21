# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_auto_20150721_1855'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='ticket',
            field=models.ForeignKey(to='services.Ticket', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='ticket',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='event',
        ),
    ]
