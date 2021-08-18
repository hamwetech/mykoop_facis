from django.conf.urls import url

from product.views import *

urlpatterns = [



      url(r'price/log/(?P<pk>[\w]+)/$', ProductVariationPriceLogListView.as_view(), name='price_log_list'),
      url(r'price/request/(?P<pk>[\w]+)/$', get_product_price, name='product_price'),
      url(r'price/list/$', ProductVariationPriceListView.as_view(), name='price_list'),
      url(r'price/create/$', ProductVariationPriceCreateView.as_view(), name='price_create'),
      url(r'price/(?P<pk>[\w]+)/$', ProductVariationPriceUpdateView.as_view(), name='price_edit'),
      url(r'variation/list/$', ProductVariationListView.as_view(), name='variation_list'),
      url(r'variation/create/$', ProductVariationView.as_view(), name='variation_create'),
      url(r'variation/(?P<pk>[\w]+)/$', ProductVariationView.as_view(), name='variation_edit'),
      url(r'unit/list/$', ProductUnitListView.as_view(), name='unit_list'),
      url(r'unit/create/$', ProductUnitCreateView.as_view(), name='unit_create'),
      url(r'unit/(?P<pk>[\w]+)/$', ProductUnitUpdateView.as_view(), name='unit_edit'),
]