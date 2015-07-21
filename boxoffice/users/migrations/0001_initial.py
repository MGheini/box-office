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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('pre_phone_number', models.CharField(blank=True, max_length=3, validators=[django.core.validators.RegexValidator(message='پیش\u200cشماره متشکل از سه رقم است.', regex='^\\d{3}$')])),
                ('phone_number', models.CharField(blank=True, max_length=10, validators=[django.core.validators.RegexValidator(message='بین ۶ تا ۱۰ رقم وارد کنید.', regex='^\\d{6,10}$')])),
                ('gender', models.CharField(blank='False', choices=[('M', 'مرد'), ('F', 'زن')], max_length=1)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('organization_name', models.CharField(max_length=255)),
                ('organization_reg_num', models.CharField(max_length=255)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
