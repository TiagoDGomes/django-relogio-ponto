# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-20 13:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Colaborador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('pis', models.CharField(max_length=25, unique=True)),
                ('verificar_digital', models.NullBooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Matricula',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField()),
                ('colaborador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Colaborador')),
            ],
        ),
        migrations.CreateModel(
            name='Parametro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('propriedade', models.CharField(max_length=25)),
                ('valor', models.CharField(max_length=100)),
                ('tipo', models.CharField(default='str', max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='RelogioPonto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.IntegerField(choices=[(1, b'Henry - Prisma')])),
            ],
        ),
        migrations.AddField(
            model_name='parametro',
            name='relogio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.RelogioPonto'),
        ),
    ]
