from django.db import transaction
from django.shortcuts import render
from django.contrib.auth.models import Permission
from bocatapp.models import User
from customer.models import ShoppingCart
from django.views.generic import FormView
from forms import UserRegistrationForm
from django.http.response import HttpResponseRedirect


def home(request):
    return render(request, 'home.html')


class RegistrationCustomerView(FormView):  # Vista de la Registracion basada en vistas de Django ( View )

    def get(self, request):
        if not request.user.is_authenticated():
            form = UserRegistrationForm()
            context = {'type': 'Customer Registration',
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
                user = create_user(form)
                password = form.cleaned_data.get('password')
                user.set_password(password)
                save_customer(user)
                save_shoppingcart(user)
                return HttpResponseRedirect("/")
            else:
                message = ""
                for field, errors in form.errors.items():
                    for error in errors:
                        message += error
                context = {
                    'form': form, 'message': message
                }
                return render(request, '../templates/forms/register_form.html', context)
        else:
            return render(request, '../templates/forbidden.html')


class RegistrationSellerView(FormView):  # Vista de la Registracion basada en vistas de Django ( View )

    def get(self, request):
        if not request.user.is_authenticated():
            form = UserRegistrationForm()
            context = {'type': 'Seller Registration',
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
                user = create_user(form)
                password = form.cleaned_data.get('password')
                user.set_password(password)
                save_seller(user)
                return HttpResponseRedirect("/")
            else:
                message = ""
                for field, errors in form.errors.items():
                    for error in errors:
                        message += error
                context = {
                    'form': form, 'message': message
                }
                return render(request, '../templates/forms/register_form.html', context)
        else:
            return render(request, '../templates/forbidden.html')


def create_user(form):
    res = User(first_name=form.cleaned_data['first_name'],
               email=form.cleaned_data['email'],
               username=form.cleaned_data['username'],
               password=form.cleaned_data['password'])
    return res


def save_customer(user):
    user.save()
    user.user_permissions.add(Permission.objects.get(codename="customer"))


def save_seller(user):
    user.save()
    user.user_permissions.add(Permission.objects.get(codename="seller"))

def save_shoppingcart(user):
    shoppingcart = ShoppingCart(customer=user)
    shoppingcart.save()
