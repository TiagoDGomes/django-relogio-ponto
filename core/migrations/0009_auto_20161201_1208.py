# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-01 12:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20161128_0833'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormatoExportacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=25)),
                ('formato', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='registroponto',
            name='exportado',
            field=models.BooleanField(default=False),
        ),
    ]
