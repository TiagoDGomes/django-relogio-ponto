# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-21 12:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_padraoexportacao'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='colaborador',
            options={'ordering': ('nome',), 'verbose_name_plural': 'colaboradores'},
        ),
        migrations.AddField(
            model_name='padraoexportacao',
            name='tamanho',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='padraoexportacao',
            name='formato',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]