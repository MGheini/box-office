# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0006_auto_20150725_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='purchased_num',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ticket_price',
            field=models.PositiveIntegerField(help_text='قیمت بلیت', verbose_name='قیمت بلیت'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ticket_type',
            field=models.CharField(max_length=255, help_text='نوع بلیت', verbose_name='نوع بلیت'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='total_capacity',
            field=models.PositiveSmallIntegerField(help_text='ظرفیت بلیت', verbose_name='ظرفیت'),
        ),
    ]
