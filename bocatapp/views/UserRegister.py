from django.db import transaction
from django.shortcuts import render
from django.contrib.auth.models import Permission
from django.views.generic import FormView
from bocatapp.forms import UserRegistrationForm
from django.http.response import HttpResponseRedirect


class RegistrationCustomerView(FormView):
    def get(self, request):
        if not request.user.is_authenticated():
            form = UserRegistrationForm()
            context = {'type': 'Registro',
                       'form': form,
                       }
            return render(request, '../templates/forms/register_form.html', context)
        else:
            return render(request, '../templates/forbidden.html')

    @transaction.atomic
    def post(self, request):
        if not request.user.is_authenticated():
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                user = form.create_user()
                password = form.cleaned_data.get('password')
                user.set_password(password)
                save_customer(user)
                return HttpResponseRedirect("/")
            else:
                message = ""
                for field, errors in form.errors.items():
                    for error in errors:
                        message += error
                context = {
                    'type': 'Registro',
                    'form': form, 'message': message
                }
                return render(request, '../templates/forms/register_form.html', context)
        else:
            return render(request, '../templates/forbidden.html')


class RegistrationSellerView(FormView):
    def get(self, request):
        if not request.user.is_authenticated():
            form = UserRegistrationForm()
            context = {'type': 'Registro de vendedor',
                       'form': form,
                       }
            return render(request, '../templates/forms/register_form.html', context)
        else:
            return render(request, '../templates/forbidden.html')

    @transaction.atomic
    def post(self, request):
        if not request.user.is_authenticated():
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                user = form.create_user()
                password = form.cleaned_data.get('password')
                user.set_password(password)
                save_seller(user)
                return HttpResponseRedirect("/")
            else:
                message = ""
                for field, errors in form.errors.items():
                    for error in errors:
                        message += error
                context = {'type': 'Registro de vendedor',
                           'form': form, 'message': message
                           }
                return render(request, '../templates/forms/register_form.html', context)
        else:
            return render(request, '../templates/forbidden.html')


def save_customer(user):
    user.save()
    user.user_permissions.add(Permission.objects.get(codename="customer"))


def save_seller(user):
    user.save()
    user.user_permissions.add(Permission.objects.get(codename="seller"))
