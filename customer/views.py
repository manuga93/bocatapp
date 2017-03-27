from django.shortcuts import render_to_response, get_object_or_404, render, redirect, get_list_or_404, render
from customer.services import OrderService
from django.template import RequestContext
from django.http.response import HttpResponseRedirect
from customer.models import Order, OrderLine, ShoppingCart, ShoppingCartLine
from seller.models import Product, Local
from django.db.models import Sum, F, FloatField
from bocatapp.decorators import permission_required
# Create your views here.

# This method is for testing the funcionality


def all_orders(request):
    try:
        orders = OrderService.find_all_orders()
        return render_to_response('orders.html', {'orders': orders}, context_instance=RequestContext(request))
    except Order.DoesNotExist:
        return render_to_response('error.html', context_instance=RequestContext(request))


def orders_by_customer(request, pk):
    orders = get_list_or_404(Order, customer=pk)
    return render_to_response('orders.html', {'orders': orders})


def order_line_by_order(request, order_id):
    try:
        orders_line = OrderService.find_order_line_by_order(order_id)
        return render_to_response('ordersLine.html', {'lines': orders_line}, context_instance=RequestContext(request))
    except OrderLine.DoesNotExist:
        return render_to_response('error.html', context_instance=RequestContext(request))


def do_order_line(request, id1):
    order_line = get_object_or_404(OrderLine, pk=id1)
    order_line.status = True
    order_line.save()
    OrderService.set_order_status(order_line.order_id)
    return HttpResponseRedirect("/customer/ordersLine/" + str(order_line.order_id))

# Vista del carrito de compra actual del customer logueado
def list_shoppingcart(request):
    current_user = request.user
    shoppingcart = ShoppingCart.objects.get(customer_id=current_user.id)
    total_price = (ShoppingCartLine.objects
                    .filter(shoppingCart_id=shoppingcart.id)
                    .aggregate(total=Sum(F('quantity')*F('product__price'), output_field=FloatField()))['total'])
    if not total_price:
        total_price = 0.0
    shoppingcart_line = ShoppingCartLine.objects.filter(shoppingCart_id=shoppingcart.id)
    return render(request, 'shoppingcart.html', {'shoppingcart_line': shoppingcart_line, 'total_price': total_price})


# Metodo para agregar un producto al carrito de compra
def add_shoppingcart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    current_user = request.user
    shoppingcart = ShoppingCart.objects.get(customer_id=current_user.id)
    shoppingcart_line_query = ShoppingCartLine.objects.filter(product_id=product.id)

    if shoppingcart_line_query:
        shoppingcart_line_query.update(quantity = F('quantity')+1)

    else:
        shoppingcart_line = ShoppingCartLine(quantity=1,
                product=product,
                shoppingCart=shoppingcart)
        shoppingcart_line.save()

    return redirect('customer.views.list_shoppingcart')


# Metodo para eliminar un producto del carrito
def remove_shoppingcart(request, pk):
    product = get_object_or_404(ShoppingCartLine, pk=pk)
    product.delete()

    return redirect('customer.views.list_shoppingcart')


@permission_required('bocatapp.customer', message='You are not a customer')
def customer_dashboard(request):
    orders_pending = OrderService.pending_orders(request.user.id)
    orders_complete = OrderService.complete_orders(request.user.id)

    context = {
        'orders_pending': orders_pending,
        'orders_complete': orders_complete
    }
    return render_to_response('customerDashboard.html', context, context_instance=RequestContext(request))


