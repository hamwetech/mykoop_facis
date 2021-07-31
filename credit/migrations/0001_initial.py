# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2021-07-15 12:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('coop', '0019_auto_20210715_1517'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CreditManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=120)),
                ('contact_person', models.CharField(blank=True, max_length=255, null=True)),
                ('contact_phone_number', models.CharField(blank=True, max_length=255, null=True)),
                ('api_username', models.CharField(blank=True, max_length=255, null=True)),
                ('api_password', models.CharField(blank=True, max_length=255, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'credit_manager',
            },
        ),
        migrations.CreateModel(
            name='CreditManagerAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('credit_manager', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='credit.CreditManager')),
                ('user', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='cm_admin', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LoanRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requested_amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('request_date', models.DateTimeField()),
                ('deadline', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('PROCESSING', 'PROCESSING'), ('ACCEPTED', 'ACCEPTED'), ('REJECTED', 'REJECTED'), ('INPROGRESS', 'INPROGRESS'), ('PAID', 'PAID')], default='PENDING', max_length=64)),
                ('paid_amount', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('last_payment_date', models.DateTimeField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('credit_manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='credit.CreditManager')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coop.CooperativeMember')),
            ],
            options={
                'db_table': 'loan_request',
            },
        ),
    ]