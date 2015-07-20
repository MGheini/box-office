# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_auto_20150720_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_subcategory',
            field=smart_selects.db_fields.ChainedForeignKey(to='services.SubCategory', chained_field='event_category', auto_choose=True, chained_model_field='event_category'),
        ),
    ]
