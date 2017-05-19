# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, render, redirect, get_list_or_404, render
from customer.services import OrderService, ReportService
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from customer.models import Order, OrderLine, ShoppingCart, ShoppingCartLine, Comment, Report
from seller.models import Product, Local, Category
from administration.models import CreditCard
from django.db.models import Sum, F, FloatField
from django.contrib import messages
from administration.forms.forms import CreditCardForm
from django.core.urlresolvers import reverse
from customer.services import CommentService
from bocatapp.decorators import permission_required
from datetime import datetime, timedelta, time
from bocatapp.views import home
from forms.forms import CommentForm, ReportForm
from customer.classes.PSCPayment import PSCPayment
from bocatapp.settings import PAYSAFECARD_API_KEY, PAYSAFECARD_ENVIROMENT, PAYSAFECARD_DEFAULT_CURRENCY
import itertools, socket, json
import re
import logging

# Create your views here.

# This method is for testing the funcionality


def recharge_account_success(request):
    payment_id = request.GET.get('payment_id', '')
    pscpayment = PSCPayment(PAYSAFECARD_API_KEY, PAYSAFECARD_ENVIROMENT)
    pscpayment.retrievePayment(payment_id)

    if pscpayment.requestIsOK():
        logging.info('Retrive payment successful.')
        logging.debug(json.dumps(pscpayment.getResponse(), indent=2))

        if pscpayment.getResponse()['status'] == 'AUTHORIZED':
            messages.add_message(request, messages.SUCCESS, 'La recarga se ha aceptado. Pronto tendrá el dinero en su cuenta.')

        elif pscpayment.getResponse()['status'] == 'SUCCESS':
            messages.add_message(request, messages.SUCCESS, '¡Su saldo ha sido actualizado con éxito!')
            logging.info('payment status success')
            logging.debug('Retrieve Reponse')
            logging.debug(json.dumps(pscpayment.getResponse(), indent=2))

        elif pscpayment.getResponse()['status'] == 'INITIATED':
            logging.info('payment is not yet processed, please visit / redirect to auth_url your received on payment creation')
            return redirect(pscpayment.getResponse()['redirect']['auth_url'])
    else:
        # retrive payment failed, handle errors
        messages.add_message(request, messages.WARNING, 'Se ha producido un error al recuperar el pago.')
        error = pscpayment.getError()
        logging.error("#### Error ####")
        logging.error("Request failed with Error: " + str(error['number']) + " - " +  error['message'])
        logging.debug('Debug information:')
        logging.debug(json.dumps(pscpayment.getResponse(), indent=2))
        logging.debug('###############')
        return redirect(home.home)

def recharge_account_failure(request):
    # payment_id = request.GET.get('payment_id', '')
    messages.add_message(request, messages.WARNING, '¡Hubo un problema al actualizar su saldo! Inténtelo de nuevo más tarde')
    return render(request, 'recharge_account.html', {})


def recharge_account_notification(request):
    payment_id = request.GET.get('payment_id', '')
    pscpayment = PSCPayment(PAYSAFECARD_API_KEY, PAYSAFECARD_ENVIROMENT)
    pscpayment.retrievePayment(payment_id)

    if pscpayment.requestIsOK():
        logging.info('Retrive payment successful.')
        logging.debug(json.dumps(pscpayment.getResponse(), indent=2))

        if pscpayment.getResponse()['status'] == 'AUTHORIZED':
            logging.info("Capturing payment")
            pscpayment.capturePayment(payment_id)

            if pscpayment.requestIsOK():
                logging.info('Capture request was successful. Checking response:')
                logging.debug(json.dumps(pscpayment.getResponse(), indent=2))

                if pscpayment.getResponse()['status'] == 'SUCCESS':
                    """
                     *                Payment OK
                     *        Here you can save the Payment
                     * process your actions here (i.e. send confirmation email etc.)
                     *  This is a fallback to notification
                     *
                    """
                else:
                    logging.error('Payment failure')
                    logging.error(json.dumps(pscpayment.getResponse(), indent=2))
            else:
                error = pscpayment.getError()
                logging.error("#### Error ####")
                logging.error("# Request failed with Error: " + str(error['number']) + " - " + error['message'])
                logging.debug('Debug information:')
                logging.debug(json.dumps(pscpayment.getResponse(), indent=2))
                logging.debug('###############')

        elif pscpayment.getResponse()['status'] == 'SUCCESS':
            # retrieved payment has success status
            # print a positive response to the customer
            logging.info('payment status success - Thank you for your purchase!')
            logging.debug('Retrieve Reponse')
            logging.debug(json.dumps(pscpayment.getResponse(), indent=2))

        elif pscpayment.getResponse()['status'] == 'INITIATED':
            # payment is iniated but not yet payed / failed
            logging.info('payment is not yet processed, please visit / redirect to auth_url your received on payment creation')

    else:
        # retrive payment failed, handle errors
        error = pscpayment.getError()
        logging.error("#### Error ####")
        logging.error("Request failed with Error: " + str(error['number']) + " - " +  error['message'])
        logging.debug('Debug information:')
        logging.debug(json.dumps(pscpayment.getResponse(), indent=2))
        logging.debug('###############')


@permission_required('bocatapp.customer', message='You are not a customer')
def recharge_account(request):
    if request.user.is_authenticated():
        pscpayment = PSCPayment(PAYSAFECARD_API_KEY, PAYSAFECARD_ENVIROMENT)
        customer_ip = socket.gethostbyname(socket.gethostname())
        domain = request.get_host()

        success_url = 'http://{domain}{path}?payment_id={{payment_id}}'.format(domain=domain, path=reverse('recharge_account_success'))
        failure_url = 'http://{domain}{path}?payment_id={{payment_id}}'.format(domain=domain, path=reverse('recharge_account_failure'))
        notification_url = 'http://bocatapp.com{path}?payment_id={{payment_id}}'.format(domain=domain, path=reverse('recharge_account_notification'))

        print(notification_url)

        pscpayment.createPayment(request.GET.get('price', ''), PAYSAFECARD_DEFAULT_CURRENCY, request.user.id, customer_ip, success_url, failure_url, notification_url)
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
            print json.dumps(pscpayment.getResponse(), indent=2)
            return render(request, 'recharge_account.html', {'error': error})
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
        orders_not_do = request.user.order_set.all().filter(status=False)
        orders_pending = {o: o.orderline_set.all() for o in orders_not_do}
        # Done orders
        orders_do = request.user.order_set.all().filter(status=True)
        orders_done = {o: o.orderline_set.all() for o in orders_do}
        return render(request, 'orders.html', {'orders_pending': orders_pending, 'orders_done': orders_done})


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
            creditcard = form.save()
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
