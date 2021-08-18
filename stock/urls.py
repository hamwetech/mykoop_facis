from stock.views import *
from django.conf.urls import url


urlpatterns = [
      url(r'item/category/edit/(?P<pk>[\w]+)/$', ItemCategoryUpdateView.as_view(), name='item_category_update'),
      url(r'item/category/list/$', ItemCategoryListView.as_view(), name='item_category_list'),
      url(r'item/category/create/$', ItemCategoryCreateView.as_view(), name='item_category_create'),

      url(r'item/price/(?P<pk>[\w]+)/$', get_item_price, name='item_price'),
      url(r'item/edit/(?P<pk>[\w]+)/$', ItemUpdateView.as_view(), name='item_update'),
      url(r'item/list/$', ItemListView.as_view(), name='item_list'),
      url(r'item/create/$', ItemCreateView.as_view(), name='item_create'),

      url(r'supplier/edit/(?P<pk>[\w]+)/$', SupplierUpdateView.as_view(), name='supplier_update'),
      url(r'supplier/list/$', SupplierListView.as_view(), name='supplier_list'),
      url(r'supplier/create/$', SupplierCreateView.as_view(), name='supplier_create'),

      url(r'commission/list/$', SalesCommissionListView.as_view(), name='commission_list'),
      url(r'commission/create/$', SalesCommissionCreateView.as_view(), name='commission_create'),
      url(r'commission/edit/(?P<pk>[\w]+)/$', SalesCommissionUpdateView.as_view(), name='commission_update'),

      url(r'supplier/user/list/(?P<supplier>[\w]+)/$', SupplierUserListView.as_view(), name="supplier_user_list"),
      url(r'supplier/user/create/(?P<supplier>[\w]+)/$', SupplierUserCreateView.as_view(), name="supplier_user_create"),

      url(r'inventory/list/$', InventoryListView.as_view(), name="inventory_list"),
      url(r'inventory/create/$', InventoryCreateView.as_view(), name="inventory_create"),
      url(r'inventory/list/(?P<supplier>[\w]+)/$', InventoryCreateView.as_view(), name="inventory_update"),

      url(r'compute/final/price/$', compute_item_price, name='compute_price'),
      url(r'token/create/$', compute_famunera_token, name='famunera_token'),
]