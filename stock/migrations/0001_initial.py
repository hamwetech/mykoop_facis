# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2021-08-18 10:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conf', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryTransactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('IN', 'IN'), ('OUT', 'OUT')], max_length=32)),
                ('batch_number', models.CharField(blank=True, max_length=255, null=True)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=20)),
                ('quantity_after', models.DecimalField(decimal_places=2, max_digits=20)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('manufacture_date', models.DateField(blank=True, null=True)),
                ('expiry_date', models.DateField(blank=True, null=True)),
                ('received_date', models.DateField(blank=True, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'inventory_transaction',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('allow_loan_request', models.BooleanField(default=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Retail Price')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=20)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'item',
            },
        ),
        migrations.CreateModel(
            name='ItemAdditionalCharges',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=160)),
                ('charge_type', models.CharField(choices=[('CHARGE', 'CHARGE'), ('DISCOUNT', 'DISCOUNT')], max_length=36)),
                ('value', models.DecimalField(decimal_places=2, max_digits=12)),
                ('value_type', models.CharField(choices=[('AMOUNT', 'AMOUNT'), ('PERCENTAGE', 'PERCENTAGE')], max_length=36)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'item_addition_charges',
            },
        ),
        migrations.CreateModel(
            name='ItemCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=255)),
                ('category_code', models.CharField(blank=True, max_length=120, null=True, unique=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.ItemCategory')),
            ],
            options={
                'db_table': 'item_category',
            },
        ),
        migrations.CreateModel(
            name='SalesCommission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('AGENT', 'AGENT'), ('COOPERATIVE', 'COOPERATIVE')], max_length=64)),
                ('commission_value', models.DecimalField(decimal_places=2, max_digits=12)),
                ('transaction_type', models.CharField(choices=[('PERCENT', 'PERCENT'), ('AMOUNT', 'AMOUNT')], max_length=64)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'sale_commission',
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=32, null=True)),
                ('email', models.CharField(blank=True, max_length=32, null=True)),
                ('contact_person', models.CharField(blank=True, max_length=32, null=True)),
                ('contact_person_phone_number', models.CharField(blank=True, max_length=32, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='supplier/logo/')),
                ('api_url', models.CharField(blank=True, max_length=255, null=True)),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
                ('token', models.TextField(blank=True, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'supplier',
            },
        ),
        migrations.CreateModel(
            name='SupplierAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('supplier', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='stock.Supplier')),
                ('user', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='supplier_admin', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='salescommission',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.Supplier'),
        ),
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.ItemCategory'),
        ),
        migrations.AddField(
            model_name='item',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='inventorytransactions',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.Item'),
        ),
        migrations.AddField(
            model_name='inventorytransactions',
            name='payment_method',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='conf.PaymentMethod'),
        ),
        migrations.AddField(
            model_name='inventorytransactions',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='stock.Supplier'),
        ),
        migrations.AlterUniqueTogether(
            name='salescommission',
            unique_together=set([('supplier', 'category')]),
        ),
    ]
