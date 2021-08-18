# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.http import JsonResponse
from django.db import transaction
from django.shortcuts import render, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from activity.models import ThematicArea, TrainingSession, ExternalTrainer, TestItem, SoilTest, SoilTestSample
from activity.forms import SoilTestSampleForm, SoilTest, TestItemForm, SoilTestForm

from conf.utils import generate_alpanumeric, log_debug, log_error


class ExtraContext(object):
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(ExtraContext, self).get_context_data(**kwargs)
        context['active'] = ['_test']
        context['title'] = 'Test'
        context.update(self.extra_context)
        return context


class TestItemCreateView(ExtraContext, CreateView):
    model = TestItem
    form_class = TestItemForm
    extra_context = {'active': ['_test', '__items']}
    success_url = reverse_lazy('activity:test_item_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(TestItemCreateView, self).form_valid(form)


class TestItemUpdateView(ExtraContext, UpdateView):
    model = TestItem
    form_class = TestItemForm
    extra_context = {'active': ['_test', '__items']}
    success_url = reverse_lazy('activity:test_item_list')


class TestItemListView(ExtraContext, ListView):
    model = TestItem
    extra_context = {'active': ['_test', '__items']}


class SoilTestListView(ExtraContext, ListView):
    model = SoilTest
    extra_context = {'active': ['_test', '__soil_test']}


class SoilTestCreateView(ExtraContext, CreateView):
    model = SoilTest
    form_class = SoilTestForm
    extra_context = {'active': ['_test', '__items']}

    def get_success_url(self):
        return reverse('activity:soil_sample_create', kwargs={'pk':self.object.pk})


class SoilTestView(View):
    template_name = 'activity/soilsample_test_form.html'

    def get(self, request, *args, **kwargs):
        form = SoilTestSampleForm
        soil_test = get_object_or_404(SoilTest, pk=self.kwargs.get('pk'))
        soil_sample = SoilTestSample.objects.filter(soil_test=soil_test)
        data = {
            'active': ['_test', '__soil_test'],
            'form': form,
            'soil_test': soil_test,
            'soil_sample': soil_sample
        }
        return render(request, self.template_name, data)

    def post(self, request, *args, **kwargs):
        sample_results = json.loads(request.POST.get("sample_results"))
        soil_test = request.POST.get("soil_test")
        try:
            with transaction.atomic():
                st = get_object_or_404(SoilTest, pk=soil_test)
                SoilTestSample.objects.filter(soil_test=st).delete()
                for v in sample_results:
                    it = get_object_or_404(TestItem, item=v.get('test_item'))
                    SoilTestSample.objects.create(
                        sample_number=v.get('sample_number'),
                        soil_test = st,
                        test_item = it,
                        measure=v.get('measure'),
                        created_by = request.user
                    )
                response = {"error": False, "message": "Saved successfully"}
        except Exception as e:
            response = {"error": True, "message": "Error occured when saving record. %s" % e}
        return JsonResponse(response)







