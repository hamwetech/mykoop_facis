from django import forms
from django.contrib.auth.models import User, Group

from conf.utils import bootstrapify
from userprofile.models import *
from coop.models import CooperativeAdmin, Cooperative


class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=150, required=True, widget=forms.PasswordInput)
    password = forms.CharField(max_length=150, required=True, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop("instance", None)

        super(UserForm, self).__init__(instance=instance, *args, **kwargs)
        if instance:
            self.fields.pop('password')
            self.fields.pop('confirm_password')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'is_superuser', 'is_active', 'username', 'password',
                  'confirm_password']


class UserProfileForm(forms.ModelForm):
    other_cooperative = forms.MultipleChoiceField(required=False,
                                                  choices=[])

    class Meta:
        model = Profile
        fields = ['msisdn', 'access_level', 'other_cooperative']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['other_cooperative'].choices = [[x.id, x.name] for x in Cooperative.objects.all()]
        self.fields['other_cooperative'].widget.attrs.update({'id': "selec_adv_1"})
        if self.request.user.profile.is_cooperative():
            al = AccessLevel.objects.filter(name="AGENT")
            if al.exists():
                al = al[0]
                self.fields['access_level'].initial = al
                self.fields['access_level'].widget=forms.HiddenInput()


class CooperativeAdminForm(forms.ModelForm):
    class Meta:
        model = CooperativeAdmin
        fields = ['cooperative']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CooperativeAdminForm, self).__init__(*args, **kwargs)
        if self.request.user.profile.is_cooperative():
            if hasattr(self.request.user, 'cooperative_admin'):
                self.fields['cooperative'].widget=forms.HiddenInput()
                self.fields['cooperative'].initial=self.request.user.cooperative_admin.cooperative



# class UserProfileForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#
#         self.user = kwargs['instance'].user if kwargs['instance'] else None
#         user_kwargs = kwargs.copy()
#         user_kwargs['instance'] = self.user
#         self.user_form = UserForm(*args, **user_kwargs)
#
#         super(UserProfileForm, self).__init__(*args, **kwargs)
#
#         self.fields.update(self.user_form.fields)
#         self.initial.update(self.user_form.initial)
#
#     def save(self, *args, **kwargs):
#         self.user_form.save(*args, **kwargs)
#         return super(UserProfileForm, self).save(*args, **kwargs)
#
#     class Meta:
#         model = Profile
#         fields = ['msisdn', 'access_level']


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'permissions']


class AccessLevelForm(forms.ModelForm):
    class Meta:
        model = AccessLevel
        fields = ['name']


class AccessLevelGroupForm(forms.ModelForm):
    class Meta:
        model = AccessLevelGroup
        fields = ['access_level', 'group']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=254, widget=forms.PasswordInput())


bootstrapify(LoginForm)
bootstrapify(AccessLevelForm)
bootstrapify(AccessLevelGroupForm)
bootstrapify(GroupForm)
bootstrapify(UserForm)
bootstrapify(UserProfileForm)
bootstrapify(CooperativeAdminForm)
