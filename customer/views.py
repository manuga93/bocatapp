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
from django.utils.translation import ugettext_lazy as _
logger = logging.getLogger('bocatapp')

# Create your views here.


def recharge_account_success(request):
    payment_id = request.GET.get('payment_id', '')
    pscpayment = PSCPayment(PAYSAFECARD_API_KEY, PAYSAFECARD_ENVIROMENT)
    pscpayment.retrievePayment(payment_id)

    if pscpayment.requestIsOK():
        logger.info(_('Retrieve payment successful.'))
        logger.debug(json.dumps(pscpayment.getResponse(), indent=2))

        if pscpayment.getResponse()['status'] == 'AUTHORIZED':
            logger.info(_("Capturing payment"))
            pscpayment.capturePayment(payment_id)
            if pscpayment.requestIsOK():
                logger.info(_('Capture request was successful. Checking response:'))
                logger.debug(json.dumps(pscpayment.getResponse(), indent=2))

                if pscpayment.getResponse()['status'] == 'SUCCESS':
                    _check_pscpayment(pscpayment)
                    messages.add_message(request, messages.SUCCESS, _('Your balance has been acted correctly!'))
                else:
                    logger.error('Payment failure')
                    logger.error(json.dumps(pscpayment.getResponse(), indent=2))
                    messages.add_message(request, messages.SUCCESS, _('The reload request has been received. Your balance will be updated soon. '))
            else:
                error = pscpayment.getError()
                logger.error("#### Error ####")
                logger.error("# Request failed with Error: " + str(error['number']) + " - " + error['message'])
                logger.debug('Debug information:')
                logger.debug(json.dumps(pscpayment.getResponse(), indent=2))
                logger.debug('###############')
                messages.add_message(request, messages.WARNING, _('There were problems connecting to PaySafeCard. Try again later!'))

        elif pscpayment.getResponse()['status'] == 'SUCCESS':
            messages.add_message(request, messages.SUCCESS, _('Your balance has been successfully updated!'))
            logger.info('Payment status success')
            logger.debug('Retrieve Reponse')
            logger.debug(json.dumps(pscpayment.getResponse(), indent=2))

        elif pscpayment.getResponse()['status'] == 'INITIATED' or pscpayment.getResponse()['status'] == 'REDIRECTED':
            logger.info(_('Payment is not yet processed, please visit / redirect to auth_url your received on payment creation'))
            return redirect(pscpayment.getResponse()['redirect']['auth_url'])
        return redirect(home.home)
    else:
        # retrive payment failed, handle errors
        messages.add_message(request, messages.WARNING, _('There was an error retrieving the payment. Try again later.'))
        error = pscpayment.getError()
        logger.error("#### Error ####")
        logger.error("Request failed with Error: " + str(error['number']) + " - " +  error['message'])
        logger.debug('Debug information:')
        logger.debug(json.dumps(pscpayment.getResponse(), indent=2))
        logger.debug('###############')
        return redirect(home.home)


def recharge_account_failure(request):
    # payment_id = request.GET.get('payment_id', '')
    messages.add_message(request, messages.WARNING, _('There was a problem updating your balance! Try again later.'))
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
                messages.add_message(request, messages.WARNING, _('There was a problem connecting to PaySafeCard, please try again later!'))
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
        # Cancel orders
        orders_cancel = request.user.order_set.all().filter(status=False, cancelled=True)
        orders_cancelled = {o: o.orderline_set.all() for o in orders_cancel}
        return render(request, 'orders.html', {'orders_pending': orders_pending, 'orders_done': orders_done,'orders_cancelled': orders_cancelled})

@permission_required('bocatapp.customer', message=_('You are not a customer'))
def cancel_order(request, pk):
    order = Order.objects.get(pk=pk)
    present = timezone.now()
    devolver = 0.0
    customer = request.user
    if order.customer.pk == request.user.id:
        if order.pickupMoment > present:
            if order.status == False:
                if order.cancelled == False:

                    tiempoRestante = order.pickupMoment-present
                    if convert_timedelta(tiempoRestante)[0]>=3:
                        devolver = float(order.totalPrice)
                    elif convert_timedelta(tiempoRestante)[0]>=2:
                        devolver = float(order.totalPrice)*0.925
                    elif convert_timedelta(tiempoRestante)[0]>=1:
                        devolver = float(order.totalPrice)*0.5
                    order.cancelled = True
                    order.save()
                    customer.amount_money = (float(customer.amount_money)+devolver)
                    customer.save()

                    messages.warning(request, unicode(_('Cancellation made. Soon we will enter ')) + str(devolver) + u'\u20ac ' + unicode(_(' in your balance.')))
                    return redirect('customer.views.orders_by_customer')
                else:
                    messages.warning(request, unicode(_('The order has already been canceled')))
                    return redirect('customer.views.orders_by_customer')
            else:
                messages.warning(request, unicode(_('Sorry, the order is already made, and it is impossible to cancel it')))
                return redirect('customer.views.orders_by_customer')
        else:
            messages.warning(request, unicode(_('The order date has already passed.')))
            return redirect('customer.views.orders_by_customer')

    else:
        messages.warning(request, unicode(_('The order you are trying to cancel does not belong to you.')))
        return redirect("/")

def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return hours, minutes, seconds

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
def checkout(request, pk, form=CreditCardForm(None)):
    update_cart_checkout(request, pk)
    if request.user.has_perm('bocatapp.customer'):
        current_user = request.user
        
        try:
            shoppingcart = ShoppingCart.objects.get(customer=current_user, checkout=False)
        except ShoppingCart.DoesNotExist:
            return render(request, 'forbidden.html')
        
        local = shoppingcart.shoppingcartline_set.all()[0].product.local
        creditcards = CreditCard.objects.filter(isDeleted=False, user=current_user)
        return render(request, 'checkout.html', {'local': local,'shoppingcart': shoppingcart, 'creditcards': creditcards, 'form': form, 'datetime': datetime.now()+timedelta(minutes=30)})
    else:
        return redirect(home.home)
        

def update_cart_checkout(request, idCart):
    idShoppingCart = idCart
    if request.user.has_perm('bocatapp.customer'):
        customer = User.objects.filter(pk=request.user.id)
        shoppingCart = ShoppingCart.objects.filter(customer_id=request.user.id, checkout=False)

        try:
            actualShoppingCart = ShoppingCart.objects.get(pk=idShoppingCart)
        except ShoppingCart.DoesNotExist:
            actualShoppingCart = None

        if not shoppingCart:
            ShoppingCart.objects.filter(pk=idShoppingCart).update(customer=customer[0])
        else:
            productsShoppingCart = ShoppingCartLine.objects.filter(shoppingCart_id=shoppingCart[0].id)
            productsActualShoppingCart = ShoppingCartLine.objects.filter(shoppingCart_id=idShoppingCart)

            if productsActualShoppingCart and productsActualShoppingCart.count() > 0:
                if int(idShoppingCart) != int(shoppingCart[0].pk):
                    shoppingCart[0].delete()
                    ShoppingCart.objects.filter(pk=idShoppingCart).update(customer=customer[0])
            else:
                if int(idShoppingCart) != int(shoppingCart[0].pk):
                    if actualShoppingCart:
                        actualShoppingCart.delete()
    else:
        actualShoppingCart = ShoppingCart.objects.filter(pk=idShoppingCart)
        actualShoppingCart.delete()


@login_required
def do_checkout(request):
    form = CreditCardForm()
    if request.user.is_authenticated():
        current_user = request.user
        # Get shopping cart
        try:
            shoppingcart = ShoppingCart.objects.get(customer_id=current_user.id, checkout=False)
        except ShoppingCart.DoesNotExist:
            return render(request, 'forbidden.html')
            
        creditcard_opt = request.POST.get('creditcard', '')
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
                            return checkout(request, shoppingcart.id, form)
                        if request.POST.get('save', '') == 'on':
                            creditcard = form.save()
                        else:
                            creditcard = None
                    elif creditcard_opt == 'balance':
                        # Other credit card
                        if current_user.amount_money < shoppingcart.total_price:
                            messages.add_message(request, messages.WARNING,
                                                 _('Choose another method of payment, you do not have enough balance!'))
                            return checkout(request, shoppingcart.id)
                        else:
                            request.user.amount_money -= shoppingcart.total_price
                            request.user.save()
                            creditcard = None
                    else:
                        creditcard = CreditCard.objects.get(id=creditcard_opt)

                    # saving order
                    new_order = Order(
                        totalPrice=shoppingcart.total_price,
                        moment=time(),
                        local=local,
                        comment=_('Add your comment'),
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
                    messages.warning(request, unicode(_('The date and time of collection must be after the current date and time. Minimum 10 min.')))
                    return checkout(request, shoppingcart.id, form)

            return render(request, 'thanks.html', {})
        else:
            messages.warning(request, unicode(_('Date or time is not correct')))
            return redirect('customer.views.checkout')
    return redirect(home.home)


# ACTUALIZAR EL CAMPO AVG RATING Y A PARTIR DE ESE ORDENAR SI SE PASA UNA PRODPIEDAD AUX
@permission_required('bocatapp.customer', message=_('You are not a customer'))
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

@permission_required('bocatapp.customer', message=_('You are not user'))
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
    try:
        local = Local.objects.get(pk=pk)
        comentarios = Comment.objects.filter(local = pk, reported=0)
        return render_to_response('comment_list.html',
                                {'comentarios': comentarios, 'local': local}, context_instance=RequestContext(request))
    except Local.DoesNotExist:
        return render(request, 'forbidden.html')

# Lista los reportes de un comentario
@permission_required('bocatapp.administrator', message=_('You are not an admin'))
def report_list(request):
    dict = ReportService.commentsWithReports()
    return render_to_response('report_list.html',
                                {'reports': dict}, context_instance=RequestContext(request))

@permission_required('bocatapp.administrator', message=_('You are not an admin'))
def report_accept(request, pk):
    ReportService.accept_report(pk)
    report = get_object_or_404(Report, pk=pk)
    return redirect('report_list')

@permission_required('bocatapp.administrator', message=_('You are not an admin'))
def report_decline(request, pk):
    ReportService.decline_report(pk)
    report = get_object_or_404(Report, pk=pk)
    return redirect('report_list')
