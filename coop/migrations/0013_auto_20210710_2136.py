# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2021-07-10 18:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('coop', '0012_memberorder_request_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberorder',
            name='accept_processing_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='processor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='memberorder',
            name='approval_reject_reason',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='memberorder',
            name='approve_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='memberorder',
            name='approved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='memberorder',
            name='confirmed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_confirm', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='memberorder',
            name='processing_reject_reason',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='memberorder',
            name='processing_start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]