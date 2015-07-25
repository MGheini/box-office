# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('services', '0003_auto_20150725_1937'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('comment_text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('rate', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='feedback',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='feedback',
            name='event',
        ),
        migrations.RemoveField(
            model_name='feedback',
            name='member',
        ),
        migrations.AddField(
            model_name='event',
            name='event_avg_rate',
            field=models.FloatField(default=0.0),
        ),
        migrations.DeleteModel(
            name='Feedback',
        ),
        migrations.AddField(
            model_name='rate',
            name='event',
            field=models.ForeignKey(to='services.Event'),
        ),
        migrations.AddField(
            model_name='rate',
            name='member',
            field=models.ForeignKey(to='users.Member'),
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
            name='rate',
            unique_together=set([('member', 'event')]),
        ),
    ]
