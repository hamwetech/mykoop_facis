from __future__ import unicode_literals
import json
import datetime
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.forms.formsets import formset_factory, BaseFormSet
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from userprofile.models import Profile, AccessLevel

from credit.models import CreditManager, LoanRequest, CreditManagerAdmin
from credit.forms import CreditManagerForm, CreditManagerUserForm
from coop.models import MemberOrder, CooperativeMember, OrderItem
from conf.utils import generate_alpanumeric, genetate_uuid4, log_error, log_debug, generate_numeric, float_to_intstring, \
    get_deleted_objects, \
    get_message_template as message_template


class ExtraContext(object):
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(ExtraContext, self).get_context_data(**kwargs)

        context.update(self.extra_context)
        return context


class CreditManagerListView(ExtraContext, ListView):
    model=CreditManager
    extra_context = {'active': ['_credit', '__cm']}


class CreditManagerCreateView(ExtraContext, CreateView):
    model = CreditManager
    form_class = CreditManagerForm
    success_url = reverse_lazy('credit:cm_list')
    extra_context = {'active': ['_credit', '__cm']}

    def get_initial(self):
        initial = super(CreditManagerCreateView, self).get_initial()
        initial['instance'] = None
        return initial


class CreditManagerUpdateView(CreditManagerCreateView, UpdateView):
    pass


class CreditManagerAdminCreateView(CreateView):
    model = CreditManager
    form_class = CreditManagerUserForm
    template_name = "credit/cm_user_form.html"
    extra_context = {'active': ['__cm']}
    success_url = reverse_lazy('credit:cm_list')

    def form_valid(self, form):
        # f = super(SupplierUserCreateView, self).form_valid(form)
        instance = None
        try:
            while transaction.atomic():
                self.object = form.save()
                if not instance:
                    self.object.set_password(form.cleaned_data.get('password'))
                self.object.save()
                pk = self.kwargs.get('cm')
                cm = get_object_or_404(CreditManager, pk=pk)
                profile = get_object_or_404(Profile, pk= self.object.id)

                profile.msisdn=form.cleaned_data.get('msisdn')
                profile.access_level=get_object_or_404(AccessLevel, name='CREDIT_MANAGER')
                profile.save()

                CreditManagerAdmin.objects.create(
                    user=self.object,
                    credit_manager = cm,
                    created_by =self.request.user
                )
        except Exception as e:
            print(e)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(CreditManagerAdminCreateView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('cm')
        context['cm'] = get_object_or_404(CreditManager, pk=pk)
        return context

    def get_initial(self):
        initial = super(CreditManagerAdminCreateView, self).get_initial()
        initial['instance'] = None
        return initial

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(CreditManagerAdminCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['instance'] = None
        return kwargs


class CreditManagerAdminListView(ExtraContext, ListView):
    model = CreditManagerAdmin
    extra_context = {'active': ['__cm']}

    def get_context_data(self, **kwargs):
        context = super(CreditManagerAdminListView, self).get_context_data(**kwargs)
        context['cm'] = self.kwargs.get('cm')
        return context


class LoanRequestListView(ExtraContext, ListView):
    model=LoanRequest
    extra_context = {'active': ['_credit', '__loan']}


class LoanRequestDetailView(ExtraContext, DetailView):
    model = LoanRequest
    extra_context = {'active': ['_credit', '__loan']}


class ApproveLoan(View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        status = self.kwargs.get('status')
        today = datetime.datetime.today()
        try:
            lq = LoanRequest.objects.get(pk=pk)
            if status == 'APPROVE':
                mo.confirm_date = today
                OrderItem.object.filter(pk=lq.order_item).update(status="APPROVED")
            if status == 'REJECT':
                lq.confirm_date = today
            lq.status = status
            lq.save()
        except Exception as e:
            log_error()

        return redirect('credit:loan_list')