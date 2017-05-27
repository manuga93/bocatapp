# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


from models import User
from datetime import date


class UserRegistrationForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    acceptation = forms.BooleanField(required=False)
    phone = forms.RegexField(regex=r'^\+?1?\d{9,15}$',
                             error_message=(
                                 _("It must be 999999999 format")))

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = _("Username")
        self.fields['first_name'].label = _("First name")
        self.fields['last_name'].label = _("Last name")
        self.fields['email'].label = _("Email")
        self.fields['password'].label = _("Password")
        self.fields['password2'].label = _("Repeat password")
        self.fields['acceptation'].label = _("I accept the terms and conditions")
        self.fields['phone'].label = _("Phone")

    def clean(self):
        cleaned_data = super(UserRegistrationForm, self).clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        acceptation = cleaned_data.get("acceptation")

        if password != password2:
            self.add_error('password2', _('Passwords dont match'))
        if not acceptation:
            self.add_error(None, _('To register you have to accept the terms and conditions'))

    def create_user(self):
        res = User(first_name=self.cleaned_data['first_name'],
                   email=self.cleaned_data['email'],
                   username=self.cleaned_data['username'],
                   password=self.cleaned_data['password'],
                   last_name=self.cleaned_data['last_name'],
                   phone=self.cleaned_data['phone'])
        return res

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password2', 'phone', 'acceptation']


class UserForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    phone = forms.RegexField(regex=r'^\+?1?\d{9,15}$',
                             error_message=(
                                 "Debe tener formato 999999999"))
    birth_date = forms.DateInput()
    avatar = forms.URLField(required=False)

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = _("Name")
        self.fields['last_name'].label = _("Surname")
        self.fields['email'].label = _("Email")
        self.fields['phone'].label = _("Phone")
        self.fields['birth_date'].label = _("Birthday")
        self.fields['birth_date'].widget.attrs['class'] = 'dateinput'
        self.fields['birth_date'].widget.attrs['readonly'] = True
        self.fields['avatar'].label = _("Avatar")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'birth_date', 'avatar']

    def clean_birth_date(self):
        date = self.cleaned_data['birth_date']
        if date is not None and date > date.today():
            raise forms.ValidationError(_("Arent you born yet?!"))
        return date


class PasswordForm(forms.ModelForm):
    old_password = forms.CharField(required=True, widget=forms.PasswordInput)
    new_password = forms.CharField(required=True, widget=forms.PasswordInput)
    password = forms.CharField(required=True, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PasswordForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].label = _("Old password")
        self.fields['new_password'].label = _("New password")
        self.fields['password'].label = _("Repeat password")
        self.non_field_errors()

    class Meta:
        model = User
        fields = ['old_password', 'new_password', 'password']

    def clean(self):
        old_password = self.cleaned_data.get('old_password')
        if not check_password(old_password, self.user.password):
            self.add_error(None, _('Old password doesnt match'))
        if self.cleaned_data.get('password') != self.cleaned_data.get('new_password'):
            self.add_error(None, _('New passwords dont match'))
        return self.cleaned_data
