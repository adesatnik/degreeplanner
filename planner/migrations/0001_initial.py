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
        migrations.CreateModel(
            name='Major',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Quarter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quarter', models.CharField(max_length=50, choices=[(b'Autumn', b'Autumn'), (b'Winter', b'Winter'), (b'Spring', b'Spring')])),
                ('year', models.IntegerField()),
                ('index', models.CharField(max_length=50)),
                ('courses', models.ManyToManyField(default=None, to='planner.Course', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=1000)),
                ('number_required', models.IntegerField()),
                ('is_filter', models.BooleanField(default=False)),
                ('filter_string', models.CharField(max_length=500, blank=True)),
                ('filter_number_of_ranges', models.IntegerField(default=0, blank=True)),
                ('hidden', models.BooleanField(default=False)),
                ('class_groups', models.ManyToManyField(to='planner.Requirement', blank=True)),
                ('classes', models.ManyToManyField(to='planner.Course', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='major',
            name='requirements',
            field=models.OneToOneField(to='planner.Requirement'),
        ),
        migrations.AddField(
            model_name='class',
            name='course',
            field=models.ForeignKey(to='planner.Course'),
        ),
        migrations.AddField(
            model_name='class',
            name='plan',
            field=models.ForeignKey(to='planner.DegreePlan'),
        ),
    ]
