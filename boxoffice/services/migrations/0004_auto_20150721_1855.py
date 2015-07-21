# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_auto_20150721_1850'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='event_category',
            new_name='category',
        ),
        migrations.RemoveField(
            model_name='event',
            name='event_subcategory',
        ),
        migrations.AddField(
            model_name='event',
            name='subcategory',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_model_field='category', chained_field='category', null=True, to='services.SubCategory'),
        ),
    ]
