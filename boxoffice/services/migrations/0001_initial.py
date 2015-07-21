# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('category_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('event_title', models.CharField(max_length=255)),
                ('event_image', models.ImageField(blank=True, upload_to='media/')),
                ('event_place', models.CharField(max_length=255)),
                ('event_description', models.TextField(blank=True)),
                ('event_date', models.DateTimeField()),
                ('event_deadline', models.DateTimeField()),
                ('submit_date', models.DateTimeField(default=datetime.datetime.now)),
                ('category', models.ForeignKey(to='services.Category')),
                ('organizer', models.ForeignKey(to='users.Organizer')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('rate', models.PositiveSmallIntegerField()),
                ('post', models.TextField()),
                ('event', models.ForeignKey(to='services.Event')),
                ('member', models.ForeignKey(to='users.Member')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('num', models.PositiveSmallIntegerField()),
                ('total_price', models.PositiveIntegerField()),
                ('order_date', models.DateField()),
                ('member', models.ForeignKey(to='users.Member')),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('subcategory_name', models.CharField(max_length=100)),
                ('category', models.ForeignKey(to='services.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('ticket_type', models.CharField(max_length=255)),
                ('ticket_price', models.PositiveIntegerField()),
                ('total_capacity', models.PositiveSmallIntegerField()),
                ('purchased_num', models.PositiveSmallIntegerField()),
                ('event', models.ForeignKey(to='services.Event', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='ticket',
            field=models.ForeignKey(to='services.Ticket'),
        ),
        migrations.AddField(
            model_name='event',
            name='subcategory',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field='category', auto_choose=True, to='services.SubCategory', chained_field='category', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='ticket',
            unique_together=set([('event', 'ticket_type')]),
        ),
        migrations.AlterUniqueTogether(
            name='feedback',
            unique_together=set([('member', 'event')]),
        ),
    ]
