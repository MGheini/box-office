# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('event_title', models.CharField(max_length=255)),
                ('event_category', models.CharField(max_length=255)),
                ('event_subcategory', models.CharField(max_length=255)),
                ('event_image', models.ImageField(blank='True', upload_to='media/')),
                ('event_place', models.CharField(max_length=255)),
                ('event_date', models.DateField()),
                ('event_description', models.TextField()),
                ('event_deadline', models.DateField()),
                ('submit_date', models.DateField()),
                ('organizer', models.ForeignKey(to='users.Organizer')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('rate', models.PositiveSmallIntegerField()),
                ('post', models.TextField()),
                ('event', models.ForeignKey(to='services.Event')),
                ('member', models.ForeignKey(to='users.Member')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('num', models.PositiveSmallIntegerField()),
                ('total_price', models.PositiveIntegerField()),
                ('order_date', models.DateField()),
                ('member', models.ForeignKey(to='users.Member')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('ticket_type', models.CharField(max_length=255)),
                ('total_num', models.PositiveSmallIntegerField()),
                ('purchased_num', models.PositiveSmallIntegerField()),
                ('ticket_price', models.PositiveIntegerField()),
                ('event', models.ForeignKey(to='services.Event')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='ticket',
            field=models.ForeignKey(to='services.Ticket'),
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
