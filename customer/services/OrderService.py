from customer.models import Order,OrderLine

#CREAR UNA VISTA PARA MIS LOCALES -> DE AHI PODER NAVEGAR A LAS ORDERS DE TUS LOCALES Y POR TANTO A TUS LINEAS DE PEDIDO Y AMCABIAR SU ESTADO
def find_all_orders():
    orders = Order.objects.all().order_by('moment')
    return orders


def find_all_orders_by_local(local):
    orders = Order.objects.all().filter(local=local)
    return orders


def find_all_orders_by_customer(customer):
    orders = Order.objects.all().filter(customer=customer)
    return orders


def find_order_line_by_order(order):
    orders_line = OrderLine.objects.all().filter(order_id=order)
    return orders_line


def set_order_status(order_id):
    order = Order.objects.get(id=order_id)
    order.set_status(True)
    order.save()


def complete_orders(customer_id):
    try:
        orders = Order.objects.filter(customer_id=customer_id).filter(status=True)
    except Order.DoesNotExist:
        orders = []
    return orders


def pending_orders(customer_id):
    try:
        orders = Order.objects.filter(customer_id=customer_id).filter(status=False)
    except Order.DoesNotExist:
        orders = []
    return orders


