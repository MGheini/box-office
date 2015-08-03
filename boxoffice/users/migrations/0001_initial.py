# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('pre_phone_number', models.CharField(blank=True, validators=[django.core.validators.RegexValidator(regex='^\\d{3}$', message='پیش\u200cشماره متشکل از سه رقم است.')], max_length=3)),
                ('phone_number', models.CharField(blank=True, validators=[django.core.validators.RegexValidator(regex='^\\d{6,10}$', message='بین ۶ تا ۱۰ رقم وارد کنید.')], max_length=10)),
                ('gender', models.CharField(choices=[('M', 'مرد'), ('F', 'زن')], blank='False', max_length=1)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'کاربر نوع مشتری',
                'verbose_name_plural': 'کاربران نوع مشتری',
            },
        ),
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('organization_name', models.CharField(max_length=255)),
                ('organization_reg_num', models.CharField(max_length=255)),
                ('has_permission_to_create_category', models.BooleanField(default=False)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'کاربر نوع برگزارکننده',
                'verbose_name_plural': 'کاربران نوع برگزارکننده',
            },
        ),
    ]
