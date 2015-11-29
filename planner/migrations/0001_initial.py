# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.IntegerField()),
                ('quarter', models.CharField(max_length=50, choices=[(b'Autumn', b'Autumn'), (b'Winter', b'Winter'), (b'Spring', b'Spring')])),
                ('taken', models.BooleanField(default=False)),
            ],
        ),
                  
   
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=150)),
                ('name', models.CharField(max_length=250)),
                ('department', models.CharField(max_length=150)),
                ('cross_listings', models.ManyToManyField(related_name='_course_cross_listings_+', to='planner.Course')),
            ],
        ),
        migrations.CreateModel(
            name='DegreePlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('slug', models.SlugField(unique=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),



    ]
