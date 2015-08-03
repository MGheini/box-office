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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('category_name', models.CharField(max_length=100)),
                ('category_glyphicon', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'verbose_name': 'دسته',
                'verbose_name_plural': 'دسته\u200cها',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('comment_text', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'نظر',
                'verbose_name_plural': 'نظرها',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
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
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('num_purchased', models.PositiveSmallIntegerField()),
                ('total_price', models.PositiveIntegerField()),
                ('order_date', models.DateTimeField(default=datetime.datetime(2015, 8, 4, 0, 26, 55, 377699))),
                ('purchase_code', models.PositiveIntegerField(default=5842669)),
                ('event', models.ForeignKey(to='services.Event', null=True)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('ticket_type', models.CharField(verbose_name='نوع بلیت', max_length=255, help_text='نوع بلیت')),
                ('ticket_price', models.PositiveIntegerField(verbose_name='قیمت بلیت', help_text='قیمت بلیت')),
                ('total_capacity', models.PositiveSmallIntegerField(verbose_name='ظرفیت', help_text='ظرفیت بلیت')),
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
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field='category', chained_field='category', to='services.SubCategory', auto_choose=True, null=True),
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
