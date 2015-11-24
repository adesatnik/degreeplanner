# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0006_auto_20151123_0754'),
    ]

    operations = [
        migrations.CreateModel(
            name='Major',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.AlterField(
            model_name='requirement',
            name='class_groups',
            field=models.ManyToManyField(to='planner.Requirement', blank=True),
        ),
        migrations.AddField(
            model_name='major',
            name='requirements',
            field=models.ManyToManyField(to='planner.Requirement'),
        ),
    ]
