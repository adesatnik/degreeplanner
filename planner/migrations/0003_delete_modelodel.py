# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0002_modelodel'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Modelodel',
        ),
    ]
