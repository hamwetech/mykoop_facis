from __future__ import unicode_literals
import json
import datetime
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.forms.formsets import formset_factory, BaseFormSet
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from credit.models import LoanRequest, CreditManager
from credit.utils import create_loan_transaction
from coop.models import MemberOrder, CooperativeMember, OrderItem
from coop.forms import OrderItemForm, MemberOrderForm
from coop.views.member import save_transaction
from conf.utils import generate_alpanumeric, genetate_uuid4, log_error, log_debug, generate_numeric, float_to_intstring, get_deleted_objects,\
get_message_template as message_template

class ExtraContext(object):
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(ExtraContext, self).get_context_data(**kwargs)
        
        context.update(self.extra_context)
        return context
    
    
class MemberOrderListView(ExtraContext, ListView):
    model = MemberOrder
    ordering = ['-create_date']
    extra_context = {'active': ['_order']}
    
    def get_queryset(self):
        queryset = super(MemberOrderListView, self).get_queryset()
        
        if self.request.user.profile.is_cooperative():
            if not self.request.user.is_superuser:
                cooperative = self.request.user.cooperative_admin.cooperative
                queryset = queryset.filter(member__cooperative=cooperative)

        if self.request.user.profile.is_supplier():
            if not self.request.user.is_superuser:
                supplier = self.request.user.supplier_admin.supplier
                order_item = OrderItem.objects.filter(item__supplier=supplier)
                o = []
                for oi in order_item:
                    o.append(oi.order)
                queryset = queryset.filter(get_supplier_orders=supplier)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(MemberOrderListView, self).get_context_data(**kwargs)
        return context


class MemberOrderCreateView(View):
    template_name = 'coop/order_item_form.html'
    
    def get(self, request, *args, **kwargs):
        
        pk = self.kwargs.get('pk')
        prod = None
        var = None
        initial = None
        extra=1
       
        form = MemberOrderForm(request=request)
        order_form = formset_factory(OrderItemForm, formset=BaseFormSet, extra=extra)
        order_formset = order_form(prefix='order', initial=initial)
        data = {
            'order_formset': order_formset,
            'form': form,
            'active': ['_order'],
        }
        return render(request, self.template_name, data)
    
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        prod = None
        var = None
        initial = None
        extra=1
        form = MemberOrderForm(request.POST, request=request)
        order_form = formset_factory(OrderItemForm, formset=BaseFormSet, extra=extra)
        order_formset = order_form(request.POST, prefix='order', initial=initial)
        try:
            with transaction.atomic():
                if form.is_valid() and order_formset.is_valid():
                    mo = form.save(commit=False)
                    mo.order_reference = generate_numeric(8, '30')
                    mo.created_by = request.user
                    mo.save()
                    price = 0
                    for orderi in order_formset:
                        os = orderi.save(commit=False)
                        os.order = mo
                        os.unit_price = os.item.price
                        os.created_by = request.user
                        os.save()
                        price += os.price
                    mo.order_price = price
                    mo.save()
                    return redirect('coop:order_list')
        except Exception as e:
            log_error()
        data = {
            'order_formset': order_formset,
            'form': form,
            'active': ['_order'],
        }
        return render(request, self.template_name, data)


class MemberOrderDetailView(ExtraContext, DetailView):
    model = MemberOrder
    extra_context = {'active': ['_order']}


class MemberOrderItemListView(ExtraContext, ListView):
    model = OrderItem
    ordering = ['-create_date']
    extra_context = {'active': ['_order']}

    def get_queryset(self):
        queryset = super(MemberOrderItemListView, self).get_queryset()

        if self.request.user.profile.is_cooperative():
            if not self.request.user.is_superuser:
                cooperative = self.request.user.cooperative_admin.cooperative
                queryset = queryset.filter(order__member__cooperative=cooperative)

        if self.request.user.profile.is_supplier():
            if not self.request.user.is_superuser:
                supplier = self.request.user.supplier_admin.supplier
                queryset = queryset.filter(item__supplier=supplier)
        return queryset


class MemberOrderDeleteView(ExtraContext, DeleteView):
    model = MemberOrder
    extra_context = {'active': ['_order']}
    success_url = reverse_lazy('coop:order_list')
    
    def get_context_data(self, **kwargs):
        #
        context = super(MemberOrderDeleteView, self).get_context_data(**kwargs)
        #
        
        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        #
        context['deletable_objects']=deletable_objects
        context['model_count']=dict(model_count).items()
        context['protected']=protected
        #
        return context
    

class MemberOrderStatusView(View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        status = self.kwargs.get('status')
        today = datetime.datetime.today()
        try:
            mo = MemberOrder.objects.get(pk=pk)
            if status == 'ACCEPT':
                mo.accept_date = today

            if status == 'SHIP':
                mo.ship_date = today
            if status == 'DELIVERED':
                mo.delivery_date = today
            if status == 'ACCEPT_DELIVERY':
                mo.delivery_accept_date = today
            if status == 'REJECT_DELIVERY':
                mo.delivery_reject_date = today
            if status == 'COLLECTED':
                mo.collect_date = today
            mo.status = status
            mo.save()
        except Exception as e:
            log_error()
        
        return redirect('coop:order_list')


class OrderItemStatusView(View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        status = self.kwargs.get('status')
        today = datetime.datetime.today()
        mm = None
        try:
            mo = OrderItem.objects.get(pk=pk)
            mm = MemberOrder.objects.get(pk=mo.order.id)
            if status == 'CONFIRMED':
                mo.confirm_date = today
                mm.status = 'PROCESSING'
                mm.save()
            #     If Loan Create Request
                if mm.request_type == "LOAN":
                    today = datetime.datetime.now()
                    lrq = LoanRequest.objects.filter(create_date__year=today.strftime("%Y"))
                    ln_cnt = lrq.count() + 1
                    reference = "LRQ/%s/%s" % (today.strftime("%y"), format(ln_cnt, '04'))
                    LoanRequest.objects.create(
                        reference = reference,
                        member=mm.member,
                        credit_manager=CreditManager.objects.all()[0],
                        requested_amount =mo.price,
                        order_item=mo,
                        request_date=datetime.datetime.now()
                    )
            #         to do send email to credit management email
            if status == 'APPROVED':
                mo.approve_date = today
            if status == 'PROCESSING':
                mo.processing_start_date = today
            if status == 'SHIP':
                mo.ship_date = today
            if status == 'DELIVERED':
                mo.delivery_date = today
            if status == 'ACCEPT_DELIVERY':
                mo.delivery_accept_date = today
            if status == 'REJECT_DELIVERY':
                mo.delivery_reject_date = today
            if status == 'COLLECTED':
                mo.collect_date = today
            mo.status = status
            mo.save()
        except Exception as e:
            print(e)
            log_error()
        if request.user.profile.is_supplier():
            return redirect('coop:order_item_list')
        return redirect('coop:order_detail', pk=mm.id)