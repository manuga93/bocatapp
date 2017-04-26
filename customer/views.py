# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, render, redirect, get_list_or_404, render
from customer.services import OrderService, ReportService
from django.template import RequestContext
from django.http.response import HttpResponseRedirect
from customer.models import Order, OrderLine, ShoppingCart, ShoppingCartLine, Comment, Report
from seller.models import Product, Local, Category
from administration.models import CreditCard
from django.db.models import Sum, F, FloatField
from django.contrib import messages
from administration.forms.forms import CreditCardForm
from django.core.urlresolvers import reverse
from bocatapp.decorators import permission_required
from datetime import datetime, timedelta, time
from bocatapp.views import home
from forms.forms import CommentForm, ReportForm
import itertools
import re

# Create your views here.

# This method is for testing the funcionality


def all_orders(request):
    try:
        orders = OrderService.find_all_orders()
        return render_to_response('orders.html', {'orders': orders}, context_instance=RequestContext(request))
    except Order.DoesNotExist:
        return render_to_response('error.html', context_instance=RequestContext(request))


@permission_required('bocatapp.customer', message='You are not a customer')
def orders_by_customer(request):
        orders = Order.objects.filter(customer=request.user.pk)
        return render_to_response('orders.html', {'orders': orders}, context_instance=RequestContext(request))


@permission_required('bocatapp.customer', message='You are not a customer')
def order_line_by_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    if order.customer.pk == request.user.pk:
        try:
            orders_line = OrderService.find_order_line_by_order(order_id)
            return render_to_response('ordersLine.html', {'lines': orders_line}, context_instance=RequestContext(request))
        except OrderLine.DoesNotExist:
            return render_to_response('error.html', context_instance=RequestContext(request))
    else:
        return redirect("/")


def do_order_line(request, id1):
    order_line = get_object_or_404(OrderLine, pk=id1)
    order_line.status = True
    order_line.save()
    OrderService.set_order_status(order_line.order_id)
    return HttpResponseRedirect("/customer/ordersLine/" + str(order_line.order_id))


# Busqueda de productos
def search_product(request, local_id):
    #Input de busqueda
    search = request.GET.get('search_input', None)
    #Local de busqueda
    local = Local.objects.get(pk=local_id)
    #Resultado de la busqueda de productos
    products = Product.objects.filter(name__icontains=unicode(search), local_id=local_id)

    #categories = Diccionario {Categoria: Productos resultantes de la busqueda en esta categoria, ...}
    if search:
        grouped = itertools.groupby(products, lambda product: product.category)
        categories = {c: p for c, p in grouped}

        #Devolvemos la pantalla de carta con la nueva lista de categorias
        return render(request, 'menu.html',
                      {'categories': categories, 'local': local})
    else:
        return redirect('seller.views.menu_list', pk=local.pk)

def objectsInCategory(cat):
    return cat.model.product_set

# Checkout view
def checkout(request, form=CreditCardForm):
    current_user = request.user
    if current_user.is_authenticated():
        shoppingcart = ShoppingCart.objects.get(customer=current_user, checkout=False)
        creditcards = CreditCard.objects.filter(isDeleted=False, user=current_user)
        return render(request, 'checkout.html', {'shoppingcart': shoppingcart, 'creditcards': creditcards, 'form': form, 'datetime': datetime.now()+timedelta(minutes=10)})
    return redirect(reverse('login'))


def do_checkout(request):
    if request.user.is_authenticated():
        current_user = request.user
        creditcard_opt = request.POST.get('creditcard', '')
        if creditcard_opt == 'new':
            # New credit card
            values = request.POST.copy()
            values['user'] = request.user.id
            expiration_date = request.POST.get('cardExpiry', '')
            # parse and split.
            if expiration_date and '/' in expiration_date:
                expireMonth = expiration_date.split('/')[0]
                expireYear = "20" + expiration_date.split('/')[1]
                values['expireMonth'] = expireMonth
                values['expireYear'] = expireYear
            form = CreditCardForm(values)
            if not form.is_valid():
                return checkout(request, form)
            creditcard = form.save()
        else:
            # Other credit card
            creditcard = CreditCard.objects.get(id=creditcard_opt)

        # Get shopping cart
        shoppingcart = ShoppingCart.objects.get(customer_id=current_user.id, checkout=False)
        shoppingcart_lines = shoppingcart.shoppingcartline_set.all()
        local = shoppingcart_lines[0].product.local
        date = request.POST.get('dateCheckout', '')
        hour = request.POST.get('hourCheckout', '')
        matchDate = re.match('(\d{2})[/.-](\d{2})[/.-](\d{4})$', date)
        matchHour = re.match('([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$', hour)

        if matchDate is not None and matchHour is not None:
            if date and '/' in date:
                dd = date.split('/')[0]
                mm = date.split('/')[1]
                aaaa = date.split('/')[2]
                # saving order
                new_order = Order(
                    totalPrice=shoppingcart.total_price,
                    moment=time(),
                    local=local,
                    comment="Añada su comentario aquí",
                    customer=current_user,
                    creditCard=creditcard,
                    pickupMoment=datetime(year=int(aaaa),month=int(mm),day=int(dd)),
                    hour=str(hour))
                new_order.save()
                # loop shoppingcart_lines
                for line in shoppingcart_lines:
                    new_order.orderline_set.create(
                        quantity=line.quantity,
                        name=line.product.name,
                        price=line.product.price
                    )

                ShoppingCart.objects.filter(customer_id=current_user.id, checkout=False).update(checkout=True)
            return render(request, 'thanks.html', {})
        else:
            messages.error(request, 'La fecha o la hora no son correctas')
            return redirect('customer.views.checkout')
    return redirect(home.home)


@permission_required('bocatapp.customer', message='You are not a customer')
def customer_dashboard(request):
    orders_pending = OrderService.pending_orders(request.user.id)
    orders_complete = OrderService.complete_orders(request.user.id)

    context = {
        'orders_pending': orders_pending,
        'orders_complete': orders_complete
    }
    return render_to_response('customerDashboard.html', context, context_instance=RequestContext(request))


@permission_required('bocatapp.customer', message='You are not a customer')
def comment_new(request, pk):
    local = get_object_or_404(Local, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.local = local
            comment.customer = request.user

            comment.save()
            return redirect('customer.views.comment_list', pk=local.pk)
    else:
        form = CommentForm()

    return render(request, 'comment_edit.html', {'form': form})

@permission_required('bocatapp.customer', message='You are not a customer')
def report_new(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.comment = comment

            report.save()
            return redirect('seller.views.local_detail', pk=comment.local.pk)
    else:
        form = ReportForm()

    return render(request, 'comment_edit.html', {'form': form})


# Lista los comentarios de un local
def comment_list(request, pk):
    local = Local.objects.get(pk=pk)
    comentarios = Comment.objects.filter(local = pk, reported=0)
    return render_to_response('comment_list.html',
                                {'comentarios': comentarios, 'local': local}, context_instance=RequestContext(request))

# Lista los reportes de un comentario
@permission_required('bocatapp.administrator', message='You are not an administrator')
def report_list(request, pk):
    reports = Report.objects.filter(comment = pk, accepted=0,decline=0)
    return render_to_response('report_list.html',
                                {'reports': reports}, context_instance=RequestContext(request))

@permission_required('bocatapp.administrator', message='You are not an administrator')
def report_accept(request, pk):
    ReportService.accept_report(pk)
    report = get_object_or_404(Report, pk=pk)
    return redirect('seller.views.local_detail', pk=report.comment.local.pk)

@permission_required('bocatapp.administrator', message='You are not an administrator')
def report_decline(request, pk):
    ReportService.decline_report(pk)
    report = get_object_or_404(Report, pk=pk)
    return redirect('customer.views.report_list', pk=report.comment.pk)
