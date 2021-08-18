from django.conf.urls import url

from activity.views.training import *
from activity.views.testing import *

urlpatterns = [
    url(r'thamatic/list/$', ThematicAreaListView.as_view(), name='thematic_list'),
    url(r'thamatic/create/$',  ThematicAreaCreateView.as_view(), name='thamatic_create'),
    url(r'thamatic/(?P<pk>[\w]+)/$', ThematicAreaUpdateView.as_view(), name='thamatic_edit'),
    url(r'training/session/(?P<pk>[\w]+)/$', TrainingSessionDetailView.as_view(), name='detail_list'),
    url(r'training/session/$', TrainingSessionListView.as_view(), name='training_list'),
    url(r'training/create/$', TrainingCreateView.as_view(), name='training_create'),
    url(r'external/create/$', ExternalTrainerCreateView.as_view(), name='external_create'),
    url(r'test/items/list/$', TestItemListView.as_view(), name='test_item_list'),
    url(r'test/items/create/$',  TestItemCreateView.as_view(), name='test_item_create'),
    url(r'test/items/(?P<pk>[\w]+)/$', TestItemUpdateView.as_view(), name='test_item_edit'),

    url(r'soil/test/list/$', SoilTestListView.as_view(), name='soil_test_list'),
    url(r'soil/test/create/$',  SoilTestCreateView.as_view(), name='soil_test_create'),
    url(r'soil/test/(?P<pk>[\w]+)/$', SoilTestCreateView.as_view(), name='soil_test_edit'),
    url(r'soil/test/sample/(?P<pk>[\w]+)/$', SoilTestView.as_view(), name='soil_sample_create'),
]