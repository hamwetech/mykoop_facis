# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from conf.models import PaymentMethod


class Supplier(models.Model):
    name = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=32, null=True, blank=True)
    email = models.CharField(max_length=32, null=True, blank=True)
    contact_person = models.CharField(max_length=32, null=True, blank=True)
    contact_person_phone_number = models.CharField(max_length=32, null=True, blank=True)
    logo = models.ImageField(upload_to='supplier/logo/', null=True, blank=True)
    api_url = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    token = models.TextField(blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'supplier'

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class SupplierAdmin(models.Model):
    user = models.OneToOneField(User, blank=True, related_name='supplier_admin')
    supplier = models.ForeignKey(Supplier, blank=True, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" % self.user.get_full_name()


class ItemCategory(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True)
    category_name = models.CharField(max_length=255)
    category_code = models.CharField(max_length=120, null=True, blank=True, unique=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "item_category"

    def __unicode__(self):
        return self.category_name


class Item(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(ItemCategory, null=True)
    # supplier = models.ForeignKey(Supplier, null=True, blank=True, on_delete=models.CASCADE)

    # supplier_price = models.DecimalField(max_digits=20, decimal_places=2)
    price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=u"Retail Price")
    quantity = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    description = models.TextField(null=True, blank=True)
    allow_loan_request = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'item'

    def __unicode__(self):
        return self.name


class ItemAdditionalCharges(models.Model):
    name = models.CharField(max_length=160)
    charge_type = models.CharField(max_length=36, choices=(('CHARGE', 'CHARGE'), ('DISCOUNT', 'DISCOUNT')))
    value = models.DecimalField(max_digits=12, decimal_places=2)
    value_type = models.CharField(max_length=36, choices=(('AMOUNT', 'AMOUNT'), ('PERCENTAGE', 'PERCENTAGE')))
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'item_addition_charges'

    def __unicode__(self):
        return "{} {}".format(self.value, self.value_type)


# @receiver(post_save, sender=ProductVariationPrice)
# def create_price_log(sender, instance, created, **kwargs):
#     if created:
#         ProductVariationPriceLog.objects.create(variation=instance)


class SalesCommission(models.Model):
    supplier = models.ForeignKey(Supplier, null=True, blank=True, on_delete=models.CASCADE)
    category = models.CharField(max_length=64, choices=(('AGENT', 'AGENT'), ('COOPERATIVE', 'COOPERATIVE')))
    commission_value = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=64, choices=(('PERCENT', 'PERCENT'), ('AMOUNT', 'AMOUNT')))
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sale_commission'
        unique_together = ['supplier', 'category']

    def __unicode__(self):
        return self.commission_value


class InventoryTransactions(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, null=True, blank=True, on_delete=models.SET_NULL)
    transaction_type = models.CharField(max_length=32, choices=(('IN','IN'), ('OUT', 'OUT')), default="OUT")
    batch_number = models.CharField(max_length=255, null=True, blank=True, unique=True)
    unit_price = models.DecimalField(max_digits=20, decimal_places=2)
    quantity = models.DecimalField(max_digits=20, decimal_places=2)
    total_price = models.DecimalField(max_digits=20, decimal_places=2)
    quantity_after = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    manufacture_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    received_date = models.DateField(null=True, blank=True)
    payment_method = models.ForeignKey(PaymentMethod, null=True, blank=True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(User, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "inventory_transaction"


@receiver(post_save, sender=InventoryTransactions)
def save_price_log(sender, instance, **kwargs):
    item = instance.item
    quantity = item.quantity
    if instance.transaction_type == 'IN':
        new_quantity = quantity + instance.quantity
    else:
        new_quantity = quantity - instance.quantity
    item.quantity = new_quantity
    item.save()



