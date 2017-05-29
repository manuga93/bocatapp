# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, render, redirect, get_list_or_404, render
from django.contrib.auth.decorators import login_required
from customer.services import OrderService, ReportService
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from customer.models import Order, OrderLine, ShoppingCart, ShoppingCartLine, Comment, Report, PSCPaymentModel
from seller.models import Product, Local, Category
from administration.models import CreditCard
from django.db.models import Sum, F, FloatField
from django.utils import timezone
from django.contrib import messages
from administration.forms.forms import CreditCardForm
from django.core.urlresolvers import reverse
from customer.services import CommentService
from bocatapp.decorators import permission_required
from bocatapp.models import User
from datetime import datetime, timedelta, time
from bocatapp.views import home
from forms.forms import CommentForm, ReportForm, RechargeForm
from customer.classes.PSCPayment import PSCPayment
from django.db import transaction
from decimal import Decimal
from bocatapp.settings import PAYSAFECARD_API_KEY, PAYSAFECARD_ENVIROMENT, PAYSAFECARD_DEFAULT_CURRENCY
import itertools
import socket
import json
import re
import logging

logger = logging.getLogger('bocatapp')

# Create your views here.


def recharge_account_success(request):
    payment_id = request.GET.get('payment_id', '')
    pscpayment = PSCPayment(PAYSAFECARD_API_KEY, PAYSAFECARD_ENVIROMENT)
    pscpayment.retrievePayment(payment_id)

    if pscpayment.requestIsOK():
        logger.info('Retrive payment successful.')
        logger.debug(json.dumps(pscpayment.getResponse(), indent=2))

        if pscpayment.getResponse()['status'] == 'AUTHORIZED':
            logger.info("Capturing payment")
            pscpayment.capturePayment(payment_id)
            if pscpayment.requestIsOK():
                logger.info('Capture request was successful. Checking response:')
                logger.debug(json.dumps(pscpayment.getResponse(), indent=2))

                if pscpayment.getResponse()['status'] == 'SUCCESS':
                    _check_pscpayment(pscpayment)
                    messages.add_message(request, messages.SUCCESS, '¡Tu saldo ha sido actualizado correctamente!')
                else:
                    logger.error('Payment failure')
                    logger.error(json.dumps(pscpayment.getResponse(), indent=2))
                    messages.add_message(request, messages.SUCCESS, 'La solicitud de recarga ha sido recibida. Pronto se actualizará tu saldo.')
            else:
                error = pscpayment.getError()
                logger.error("#### Error ####")
                logger.error("# Request failed with Error: " + str(error['number']) + " - " + error['message'])
                logger.debug('Debug information:')
                logger.debug(json.dumps(pscpayment.getResponse(), indent=2))
                logger.debug('###############')
                messages.add_message(request, messages.WARNING, 'Hubo problemas para conectar con PaySafeCard. ¡Inténtalo de nuevo más tarde!')

        elif pscpayment.getResponse()['status'] == 'SUCCESS':
            messages.add_message(request, messages.SUCCESS, 'Tu saldo ha sido actualizado con éxito!')
            logger.info('Payment status success')
            logger.debug('Retrieve Reponse')
            logger.debug(json.dumps(pscpayment.getResponse(), indent=2))

        elif pscpayment.getResponse()['status'] == 'INITIATED' or pscpayment.getResponse()['status'] == 'REDIRECTED':
            logger.info('Payment is not yet processed, please visit / redirect to auth_url your received on payment creation')
            return redirect(pscpayment.getResponse()['redirect']['auth_url'])
        return redirect(home.home)
    else:
        # retrive payment failed, handle errors
        messages.add_message(request, messages.WARNING, 'Se ha producido un error al recuperar el pago. Inténtalo de nuevo más tarde.')
        error = pscpayment.getError()
        logger.error("#### Error ####")
        logger.error("Request failed with Error: " + str(error['number']) + " - " +  error['message'])
        logger.debug('Debug information:')
        logger.debug(json.dumps(pscpayment.getResponse(), indent=2))
        logger.debug('###############')
        return redirect(home.home)


def recharge_account_failure(request):
    # payment_id = request.GET.get('payment_id', '')
    messages.add_message(request, messages.WARNING, '¡Hubo un problema al actualizar tu saldo! Inténtalo de nuevo más tarde.')
    return render(request, 'recharge_account.html', {'form': RechargeForm()})


def _check_pscpayment(pscpayment):
    amount = pscpayment.getResponse()['amount']
    currency = pscpayment.getResponse()['currency']
    customer_ip = pscpayment.getResponse()['customer']['ip']
    psc_id = pscpayment.getResponse()['id']
    customer_id = pscpayment.getResponse()['customer']['id']
    pscpayment = {
        'amount': amount,
        'currency': currency,
        'customer_ip': customer_ip,
        'psc_id': psc_id,
        'customer_id': customer_id,
    }
    userModel = User.objects.filter(id=customer_id).first()
    if userModel:
        psc = PSCPaymentModel.objects.filter(psc_id=psc_id).first()
        if psc:
            logger.error('Payment was already done!')
        else:
            psc = PSCPaymentModel(**pscpayment).save()
            logger.info('Payment has been saved!')
            userModel.amount_money += Decimal(amount)
            userModel.save()
            logger.info('Balance for user {} has been updated'.format(customer_id))
        logger.error('Payment successful')
        return JsonResponse({'response': 'Success'})


@transaction.atomic
def recharge_account_notification(request):
    payment_id = request.GET.get('payment_id', '')
    pscpayment = PSCPayment(PAYSAFECARD_API_KEY, PAYSAFECARD_ENVIROMENT)
    pscpayment.retrievePayment(payment_id)

    if pscpayment.requestIsOK():
        logger.info('Retrive payment successful.')
        logger.debug(json.dumps(pscpayment.getResponse(), indent=2))

        if pscpayment.getResponse()['status'] == 'AUTHORIZED':
            logger.info("Capturing payment")
            pscpayment.capturePayment(payment_id)

            if pscpayment.requestIsOK():
                logger.info('Capture request was successful. Checking response:')
                logger.debug(json.dumps(pscpayment.getResponse(), indent=2))

                if pscpayment.getResponse()['status'] == 'SUCCESS':
                    _check_pscpayment(pscpayment)
                else:
                    logger.error('Payment failure')
                    logger.error(json.dumps(pscpayment.getResponse(), indent=2))
                    return JsonResponse({'response': 'error'})
            else:
                error = pscpayment.getError()
                logger.error("#### Error ####")
                logger.error("# Request failed with Error: " + str(error['number']) + " - " + error['message'])
                logger.debug('Debug information:')
                logger.debug(json.dumps(pscpayment.getResponse(), indent=2))
                logger.debug('###############')
                return JsonResponse({'response': error['message']})
        return JsonResponse({'response': pscpayment.getResponse()})
    else:
        # retrive payment failed, handle errors
        error = pscpayment.getError()
        logger.error("#### Error ####")
        logger.error("Request failed with Error: " + str(error['number']) + " - " +  error['message'])
        logger.debug('Debug information:')
        logger.debug(json.dumps(pscpayment.getResponse(), indent=2))
        logger.debug('###############')
        return JsonResponse({'response': error['message']})


@permission_required('bocatapp.customer', message='You are not a customer')
def recharge_account(request):

    if request.user.is_authenticated():
        if request.method == 'POST':

            form = RechargeForm(request.POST or None)
            if not form.is_valid():
                pscs = PSCPaymentModel.objects.filter(customer=request.user)
                return render(request, 'recharge_account.html', { 'form': form, 'transactions': pscs })

            amount = str(form.cleaned_data['amount'])
            pscpayment = PSCPayment(PAYSAFECARD_API_KEY, PAYSAFECARD_ENVIROMENT)
            customer_ip = socket.gethostbyname(socket.gethostname())
            domain = request.get_host()

            success_url = 'http://{domain}{path}?payment_id={{payment_id}}'.format(domain=domain, path=reverse('recharge_account_success'))
            failure_url = 'http://{domain}{path}?payment_id={{payment_id}}'.format(domain=domain, path=reverse('recharge_account_failure'))
            notification_url = 'http://bocatapp.com{path}?payment_id={{payment_id}}'.format(domain=domain, path=reverse('recharge_account_notification'))

            pscpayment.createPayment(amount, PAYSAFECARD_DEFAULT_CURRENCY, request.user.id, customer_ip, success_url, failure_url, notification_url)
            if pscpayment.requestIsOK():
                # check if the createpayment request was successful
                # redirect customer to payment page
                return redirect(pscpayment.getResponse()['redirect']['auth_url'])

            else:
                messages.add_message(request, messages.WARNING, '¡Hubo un problema al conectar con PaySafeCard, ¡inténtelo de nuevo más tarde!')
                # create payment failed, handle errors
                error = pscpayment.getError()
                # print "#### Error ####"
                # print "Create Request failed with Error: " + str(error['number']) + " - "+  error['message']
                logger.error(json.dumps(pscpayment.getResponse(), indent=2))
                pscs = PSCPaymentModel.objects.filter(customer=request.user)
                return render(request, 'recharge_account.html', {'error': error, 'form': form, 'transactions': pscs })
        else:
            # Normal GET request (most likely)
            pscs = PSCPaymentModel.objects.filter(customer=request.user)
            return render(request, 'recharge_account.html', {'form': RechargeForm(), 'transactions': pscs})
    else:
        return redirect(home.home)

def all_orders(request):
    try:
        orders = OrderService.find_all_orders()
        return render_to_response('orders.html', {'orders': orders}, context_instance=RequestContext(request))
    except Order.DoesNotExist:
        return render_to_response('error.html', context_instance=RequestContext(request))


@permission_required('bocatapp.customer', message='You are not a customer')
def orders_by_customer(request):
        # Pending orders
        orders_not_do = request.user.order_set.all().filter(status=False, cancelled=False)
        orders_pending = {o: o.orderline_set.all() for o in orders_not_do}
        # Done orders
        orders_do = request.user.order_set.all().filter(status=True, cancelled=False)
        orders_done = {o: o.orderline_set.all() for o in orders_do}
        # Done orders
        orders_cancel = request.user.order_set.all().filter(status=False, cancelled=True)
        orders_cancelled = {o: o.orderline_set.all() for o in orders_cancel}
        return render(request, 'orders.html', {'orders_pending': orders_pending, 'orders_done': orders_done,'orders_cancelled': orders_cancelled})

@permission_required('bocatapp.customer', message='You are not a customer')
def cancel_order(request, pk):
    order = Order.objects.get(pk=pk)
    present = timezone.now()
    if order.customer.pk == request.user.id:
        if order.pickupMoment > present:
            if order.status == False:
                if order.cancelled == False:

                    order.cancelled = True
                    order.save()
                    return redirect('customer.views.orders_by_customer')
                else:
                    messages.warning(request, u'El pedido ya ha sido cancelado')
                    return redirect('customer.views.orders_by_customer')
            else:
                messages.warning(request, u'Lo sentimos, el pedido ya esta realizado, y es imposible cancelarlo')
                return redirect('customer.views.orders_by_customer')
        else:
            messages.warning(request, u'La fecha del pedido ya ha pasado.')
            return redirect('customer.views.orders_by_customer')

    else:
        messages.warning(request, u'El pedido que intentas cancelar no te pertenece.')
        return redirect("/")

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
        categories = dict((p.category, products.filter(category_id=p.category.id)) for p in products)
        #grouped = itertools.groupby(products, lambda product: product.category)
        #categories = {c: p for c, p in grouped}

        #Devolvemos la pantalla de carta con la nueva lista de categorias
        return render(request, 'menu.html',
                      {'categories': categories, 'local': local})
    else:
        return redirect('seller.views.menu_list', pk=local.pk)

def objectsInCategory(cat):
    return cat.model.product_set

# Checkout view
@login_required
def checkout(request, form=CreditCardForm(None)):
    current_user = request.user
    shoppingcart = ShoppingCart.objects.get(customer=current_user, checkout=False)
    creditcards = CreditCard.objects.filter(isDeleted=False, user=current_user)
    return render(request, 'checkout.html', {'shoppingcart': shoppingcart, 'creditcards': creditcards, 'form': form, 'datetime': datetime.now()+timedelta(minutes=10)})

@login_required
def do_checkout(request):
    if request.user.is_authenticated():
        current_user = request.user
        # Get shopping cart
        shoppingcart = ShoppingCart.objects.get(customer_id=current_user.id, checkout=False)
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
            if request.POST.get('save', '') == 'on':
                creditcard = form.save()
            else:
                creditcard = None
        elif creditcard_opt == 'balance':
            # Other credit card
            if current_user.amount_money < shoppingcart.total_price:
                messages.add_message(request, messages.WARNING, 'Elige otro método de pago, ¡no tienes suficiente saldo!')
                return checkout(request)
            else:
                request.user.amount_money -= shoppingcart.total_price
                request.user.save()
                creditcard = None
        else:
            creditcard = CreditCard.objects.get(id=creditcard_opt)

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
                hourMoment = hour.split(':')[0]
                minutesMoment = hour.split(':')[1]

                momentOrder = datetime(year=int(aaaa),month=int(mm),day=int(dd), hour=int(hourMoment), minute=int(minutesMoment))
                present = datetime.now()
                differenceDates = (momentOrder - present).total_seconds()/60

                if present < momentOrder and differenceDates > 9:
                    # saving order
                    new_order = Order(
                        totalPrice=shoppingcart.total_price,
                        moment=time(),
                        local=local,
                        comment="Añada su comentario aquí",
                        customer=current_user,
                        creditCard=creditcard,
                        pickupMoment=momentOrder)
                    new_order.save()
                    # loop shoppingcart_lines
                    for line in shoppingcart_lines:
                        new_order.orderline_set.create(
                            quantity=line.quantity,
                            name=line.product.name,
                            price=line.product.price
                        )

                    ShoppingCart.objects.filter(customer_id=current_user.id, checkout=False).update(checkout=True)

                else:
                    messages.warning(request, u'La fecha y hora de recogida debe ser posterior a la fecha y hora actual. Mínimo 10 min.')
                    return checkout(request, form)

            return render(request, 'thanks.html', {})
        else:
            messages.warning(request, u'La fecha o la hora no son correctas')
            return redirect('customer.views.checkout')
    return redirect(home.home)


# ACTUALIZAR EL CAMPO AVG RATING Y A PARTIR DE ESE ORDENAR SI SE PASA UNA PRODPIEDAD AUX
@permission_required('bocatapp.customer', message='No eres un usuario')
def comment_new(request, pk):
    local = get_object_or_404(Local, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.local = local
            comment.customer = request.user
            comment.save()
            update_avg_rating(local.pk)
            return redirect('customer.views.comment_list', pk=local.pk)
    else:
        form = CommentForm()

    return render(request, 'comment_edit.html', {'form': form, "local": local})


def update_avg_rating(local_id):
    local = get_object_or_404(Local, pk=local_id)
    aux = float(CommentService.get_stars(local.pk))
    local.avg_rating = aux
    local.save()

@permission_required('bocatapp.customer', message='No eres un usuario')
def report_new(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.comment = comment
            report.customer = request.user
            report.save()
            return redirect('comment_list', pk=comment.local.pk)
    else:
        form = ReportForm()

    return render(request, 'report_edit.html', {'form': form})


# Lista los comentarios de un local
def comment_list(request, pk):
    local = Local.objects.get(pk=pk)
    comentarios = Comment.objects.filter(local = pk, reported=0)
    return render_to_response('comment_list.html',
                                {'comentarios': comentarios, 'local': local}, context_instance=RequestContext(request))

# Lista los reportes de un comentario
@permission_required('bocatapp.administrator', message='No eres un administrador')
def report_list(request):
    dict = ReportService.commentsWithReports()
    return render_to_response('report_list.html',
                                {'reports': dict}, context_instance=RequestContext(request))

@permission_required('bocatapp.administrator', message='No eres un administrador')
def report_accept(request, pk):
    ReportService.accept_report(pk)
    report = get_object_or_404(Report, pk=pk)
    return redirect('report_list')

@permission_required('bocatapp.administrator', message='No eres un administrador')
def report_decline(request, pk):
    ReportService.decline_report(pk)
    report = get_object_or_404(Report, pk=pk)
    return redirect('report_list')
