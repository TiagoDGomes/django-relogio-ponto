# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-28 08:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_delete_padraoexportacao'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='parametro',
            unique_together=set([('relogio', 'propriedade')]),
        ),
    ]
