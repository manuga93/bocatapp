# -*- coding: utf-8 -*-
from django import forms
from models import User


class UserRegistrationForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.RegexField(regex=r'^\+?1?\d{9,15}$',
                             error_message=(
                                 "Debe tener formato 999999999"))

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Usuario"
        self.fields['first_name'].label = "Nombre"
        self.fields['last_name'].label = "Apellidos"
        self.fields['email'].label = "Correo"
        self.fields['password'].label = "Contraseña"
        self.fields['phone'].label = "Teléfono"

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
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'phone']


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
        self.fields['first_name'].label = "Nombre"
        self.fields['last_name'].label = "Apellidos"
        self.fields['email'].label = "Correo"
        self.fields['phone'].label = "Teléfono"
        self.fields['birth_date'].label = "Cumpleaños"
        self.fields['birth_date'].widget.attrs['class'] = 'dateinput'
        self.fields['avatar'].label = "Avatar (URL)"

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'birth_date', 'avatar']
