# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.forms.formsets import formset_factory, BaseFormSet
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.views.generic import View, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db import transaction

from django.contrib.auth.models import User, Group

from conf.utils import log_debug, log_error
from stock.models import *
from stock.forms import *
from userprofile.models import Profile, AccessLevel
from product.api.fanumera import FamuneraAPI

class ExtraContext(object):
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(ExtraContext, self).get_context_data(**kwargs)
        context['active'] = ['_union_prod']
        context['title'] = 'Country'
        context.update(self.extra_context)
        return context


class SupplierCreateView(ExtraContext, CreateView):
    model = Supplier
    form_class = SupplierForm
    extra_context = {'active': ['_union_prod', '__supplier']}
    success_url = reverse_lazy('stock:supplier_list')


class SupplierUpdateView(ExtraContext, UpdateView):
    model = Supplier
    form_class = SupplierForm
    extra_context = {'active': ['__supplier']}
    success_url = reverse_lazy('stock:supplier_list')


class SupplierListView(ExtraContext, ListView):
    model = Supplier
    extra_context = {'active': ['__supplier']}


class SupplierUserCreateView(CreateView):
    model = User
    form_class = SupplierUserForm
    template_name = "stock/supplier_user_form.html"
    extra_context = {'active': ['__supplier']}
    success_url = reverse_lazy('stock:supplier_list')

    def form_valid(self, form):
        # f = super(SupplierUserCreateView, self).form_valid(form)
        instance = None
        try:
            while transaction.atomic():
                self.object = form.save()
                if not instance:
                    self.object.set_password(form.cleaned_data.get('password'))
                self.object.save()
                pk = self.kwargs.get('supplier')
                supplier = get_object_or_404(Supplier, pk=pk)
                profile = get_object_or_404(Profile, pk=self.object.id)

                profile.msisdn = form.cleaned_data.get('msisdn')
                profile.access_level = get_object_or_404(AccessLevel, pk=3)
                profile.save()

                SupplierAdmin.objects.create(
                    user=self.object,
                    supplier=supplier,
                    created_by=self.request.user
                )
        except Exception as e:
            print(e)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(SupplierUserCreateView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('supplier')
        context['supplier'] = get_object_or_404(Supplier, pk=pk)
        return context

    def get_initial(self):
        initial = super(SupplierUserCreateView, self).get_initial()
        initial['instance'] = None
        return initial

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(SupplierUserCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['instance'] = None
        return kwargs


class SupplierUserListView(ExtraContext, ListView):
    model = SupplierAdmin
    extra_context = {'active': ['__supplier']}

    def get_context_data(self, **kwargs):
        context = super(SupplierUserListView, self).get_context_data(**kwargs)
        context['id'] = self.kwargs.get('supplier')
        return context


class ItemCreateView(ExtraContext, CreateView):
    model = Item
    form_class = ItemForm
    extra_context = {'active': ['__item']}
    success_url = reverse_lazy('stock:item_list')

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ItemCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        initial = None
        context = super(ItemCreateView, self).get_context_data(**kwargs)
        iformset = formset_factory(ItemAdditionChargesForm, formset=BaseFormSet, extra=1)
        formset = iformset(prefix='item_addition', initial=initial)
        context['formset'] = formset
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(ItemCreateView, self).form_valid(form)


class ItemUpdateView(ExtraContext, UpdateView):
    model = Item
    form_class = ItemForm
    extra_context = {'active': ['__item']}
    success_url = reverse_lazy('stock:item_list')

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ItemUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['request'] = self.request
        return kwargs


class ItemListView(ExtraContext, ListView):
    model = Item
    extra_context = {'active': ['__item']}

    def get_queryset(self):
        queryset = super(ItemListView, self).get_queryset()

        if self.request.user.profile.is_supplier():
            if not self.request.user.is_superuser:
                supplier = self.request.user.supplier_admin.supplier
                queryset = queryset.filter(supplier=supplier)
        return queryset


class SalesCommissionCreateView(ExtraContext, CreateView):
    model = SalesCommission
    form_class = SalesCommissionForm
    extra_context = {'active': ['_union_prod', '__commission']}
    success_url = reverse_lazy('stock:commission_list')


class SalesCommissionUpdateView(ExtraContext, UpdateView):
    model = SalesCommission
    form_class = SalesCommissionForm
    extra_context = {'active': ['__commission']}
    success_url = reverse_lazy('stock:commission_list')


class SalesCommissionListView(ExtraContext, ListView):
    model = SalesCommission
    extra_context = {'active': ['__commission']}


class ItemCategoryListView(ExtraContext, ListView):
    model = ItemCategory
    extra_context = {'active': ['__item']}


class ItemCategoryCreateView(ExtraContext, CreateView):
    model = ItemCategory
    form_class = ItemCategoryForm
    extra_context = {'active': ['__item']}
    success_url = reverse_lazy('stock:item_category_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(ItemCategoryCreateView, self).form_valid(form)


class ItemCategoryUpdateView(ExtraContext, UpdateView):
    model = ItemCategory
    form_class = ItemCategoryForm
    extra_context = {'active': ['__item']}
    success_url = reverse_lazy('stock:item_category_list')


class InventoryListView(ExtraContext, ListView):
    model = InventoryTransactions
    extra_context = {'active': ['_inventory']}


class InventoryCreateView(ExtraContext, CreateView):
    model = InventoryTransactions
    form_class = InventoryForm
    extra_context = {'active': ['_inventory']}
    success_url = reverse_lazy('stock:inventory_list')


def get_item_price(request, pk):
    try:
        pp = Item.objects.get(pk=pk)
        return JsonResponse({"price": pp.price})
    except Exception:
        return JsonResponse({"price": "error"})


@csrf_exempt
def compute_item_price(request):
    payload = request.POST.get('payload')
    supplier_price = float(request.POST.get('supplier_price'))

    retail_price = 0
    charge = 0

    for data in json.loads(payload):

        if data['value']:
            charge_type = data['charge_type']
            value = float(data['value'])
            value_type = data['value_type']

            if value_type == "PERCENTAGE":
                v = supplier_price * float(value / 100)

            if value_type == "AMOUNT":
                v = value

            if charge_type == "DISCOUNT":
                charge += - float(v)

            if charge_type == "CHARGE":
                charge += float(v)

    retail_price = supplier_price + charge
    print(retail_price)

    return JsonResponse({"retail_price": retail_price})


@csrf_exempt
def compute_famunera_token(request):
    try:
        clientId = request.POST.get("username")
        clientSecret = request.POST.get("password")

        fapi = FamuneraAPI({})
        pl = {
            "clientId": clientId,
            "clientSecret": clientSecret
        }
        gt = fapi.create_token(pl)
        return JsonResponse({"token": gt.get("token")})
    except Exception as e:
        log_error()
        return JsonResponse({"token": ""})
