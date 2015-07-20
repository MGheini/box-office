# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='gender',
            field=models.CharField(blank='False', max_length=1, choices=[('M', 'Male'), ('F', 'Female')]),
        ),
        migrations.AddField(
            model_name='member',
            name='phone_number',
            field=models.CharField(blank=True, max_length=10, validators=[django.core.validators.RegexValidator(message='بین ۶ تا ۱۰ رقم وارد کنید.', regex='^\\d{6,10}$')]),
        ),
        migrations.AddField(
            model_name='member',
            name='pre_phone_number',
            field=models.CharField(blank=True, max_length=3, validators=[django.core.validators.RegexValidator(message='پیش\u200cشماره متشکل از سه رقم است.', regex='^\\d{3}$')]),
        ),
    ]
