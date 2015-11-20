# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quarter1',
            name='courses',
        ),
        migrations.AddField(
            model_name='quarter',
            name='index',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Quarter1',
        ),
    ]
