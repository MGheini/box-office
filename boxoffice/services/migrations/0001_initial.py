# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100)),
                ('category_glyphicon', models.CharField(max_length=30, blank=True, null=True)),
            ],
            options={
                'verbose_name': 'دسته',
                'verbose_name_plural': 'دسته\u200cها',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('comment_text', models.CharField(max_length=200)),
                ('datetime', models.DateTimeField(default=datetime.datetime.now)),
                ('like_num', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'نظر',
                'verbose_name_plural': 'نظرها',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('event_title', models.CharField(max_length=255)),
                ('event_image', models.ImageField(upload_to='media/', blank=True, default='media/noimage.png')),
                ('event_place', models.CharField(max_length=255)),
                ('event_description', models.TextField(blank=True)),
                ('event_date', models.DateField()),
                ('event_time', models.TimeField()),
                ('event_deadline_date', models.DateField()),
                ('event_deadline_time', models.TimeField()),
                ('submit_date', models.DateTimeField(default=datetime.datetime.now)),
                ('event_avg_rate', models.FloatField(default=0.0)),
                ('category', models.ForeignKey(to='services.Category')),
                ('organizer', models.ForeignKey(to='users.Organizer')),
            ],
            options={
                'verbose_name': 'رویداد',
                'verbose_name_plural': 'رویدادها',
            },
        ),
        migrations.CreateModel(
            name='LikeComment',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('comment', models.ForeignKey(to='services.Comment')),
                ('member', models.ForeignKey(to='users.Member')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('num_purchased', models.PositiveSmallIntegerField()),
                ('total_price', models.PositiveIntegerField()),
                ('order_date', models.DateTimeField(default=datetime.datetime.now)),
                ('purchase_code', models.PositiveIntegerField()),
                ('first_chair_offset', models.IntegerField(default=0)),
                ('event', models.ForeignKey(to='services.Event')),
                ('member', models.ForeignKey(to='users.Member')),
            ],
            options={
                'verbose_name': 'سفارش',
                'verbose_name_plural': 'سفارش\u200cها',
            },
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('rate', models.PositiveSmallIntegerField()),
                ('event', models.ForeignKey(to='services.Event')),
                ('member', models.ForeignKey(to='users.Member')),
            ],
            options={
                'verbose_name': 'امتیاز',
                'verbose_name_plural': 'امتیازها',
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('subcategory_name', models.CharField(max_length=100)),
                ('category', models.ForeignKey(to='services.Category')),
            ],
            options={
                'verbose_name': 'زیردسته',
                'verbose_name_plural': 'زیردسته\u200cها',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('ticket_type', models.CharField(max_length=20)),
                ('ticket_price', models.PositiveIntegerField()),
                ('total_capacity', models.PositiveSmallIntegerField()),
                ('purchased_num', models.PositiveSmallIntegerField(default=0)),
                ('event', models.ForeignKey(to='services.Event')),
            ],
            options={
                'verbose_name': 'بلیت',
                'verbose_name_plural': 'بلیت\u200cها',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='ticket',
            field=models.ForeignKey(to='services.Ticket'),
        ),
        migrations.AddField(
            model_name='event',
            name='subcategory',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field='category', to='services.SubCategory', auto_choose=True, chained_field='category'),
        ),
        migrations.AddField(
            model_name='comment',
            name='event',
            field=models.ForeignKey(to='services.Event'),
        ),
        migrations.AddField(
            model_name='comment',
            name='member',
            field=models.ForeignKey(to='users.Member'),
        ),
        migrations.AlterUniqueTogether(
            name='ticket',
            unique_together=set([('event', 'ticket_type')]),
        ),
        migrations.AlterUniqueTogether(
            name='rate',
            unique_together=set([('member', 'event')]),
        ),
    ]
