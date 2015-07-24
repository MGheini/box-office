# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_auto_20150725_2104'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'دسته\u200cها', 'verbose_name': 'دسته'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name_plural': 'نظرها', 'verbose_name': 'نظر'},
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'verbose_name_plural': 'رویدادها', 'verbose_name': 'رویداد'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name_plural': 'سفارش\u200cها', 'verbose_name': 'سفارش'},
        ),
        migrations.AlterModelOptions(
            name='rate',
            options={'verbose_name_plural': 'امتیازها', 'verbose_name': 'امتیاز'},
        ),
        migrations.AlterModelOptions(
            name='subcategory',
            options={'verbose_name_plural': 'زیردسته\u200cها', 'verbose_name': 'زیردسته'},
        ),
        migrations.AlterModelOptions(
            name='ticket',
            options={'verbose_name_plural': 'بلیت\u200cها', 'verbose_name': 'بلیت'},
        ),
    ]
