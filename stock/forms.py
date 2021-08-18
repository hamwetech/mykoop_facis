from django import forms
from stock.models import *
from conf.utils import bootstrapify


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        exclude = ['create_date', 'update_date']


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ['create_date', 'update_date', 'created_by']

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super(ItemForm, self).__init__(*args, **kwargs)
        if hasattr(request.user, 'supplier_admin'):
            self.fields['supplier'].widget = forms.HiddenInput()
            self.fields['supplier'].initial = 1

    def clean(self):
        supplier_price = self.cleaned_data.get('supplier_price')
        price = self.cleaned_data.get('price')
        if supplier_price > price:
            raise forms.ValidationError('Supplier price cannot be higher than the retail price')


class SupplierUserForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=150, required=True, widget=forms.PasswordInput)
    password = forms.CharField(max_length=150, required=True, widget=forms.PasswordInput)
    msisdn = forms.CharField(max_length=150)

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop("instance", None)
        print(instance)
        super(SupplierUserForm, self).__init__(*args, **kwargs)
        if instance:
            self.fields.pop('password')
            self.fields.pop('confirm_password')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'msisdn', 'is_active', 'username', 'password',
                  'confirm_password']


class SalesCommissionForm(forms.ModelForm):
    class Meta:
        model = SalesCommission
        exclude = ['create_date', 'update_date']


class ItemAdditionChargesForm(forms.ModelForm):
    class Meta:
        model = ItemAdditionalCharges
        exclude = ['create_date', 'update_date']


class ItemCategoryForm(forms.ModelForm):
    class Meta:
        model = ItemCategory
        exclude = ['create_date', 'update_date']


class InventoryForm(forms.ModelForm):
    class Meta:
        model = InventoryTransactions
        exclude = ['create_date', 'update_date', 'quantity_after', 'created_by']


bootstrapify(InventoryForm)
bootstrapify(SupplierForm)
bootstrapify(ItemForm)
bootstrapify(ItemCategoryForm)
bootstrapify(ItemAdditionChargesForm)
bootstrapify(SupplierUserForm)
bootstrapify(SalesCommissionForm)