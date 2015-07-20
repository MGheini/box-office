# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('category_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('subcategory_name', models.CharField(max_length=100)),
                ('category', models.ForeignKey(to='services.Category')),
            ],
        ),
        migrations.RenameField(
            model_name='ticket',
            old_name='total_num',
            new_name='total_capacity',
        ),
        migrations.AlterField(
            model_name='event',
            name='event_category',
            field=models.ForeignKey(to='services.Category'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_deadline',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_description',
            field=models.TextField(blank='True'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_place',
            field=models.CharField(max_length=255, blank='True'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_subcategory',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_model_field='category', to='services.SubCategory', chained_field='category'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_title',
            field=models.CharField(max_length=255, blank='True'),
        ),
        migrations.AlterField(
            model_name='event',
            name='submit_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
