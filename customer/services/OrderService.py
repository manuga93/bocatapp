from customer.models import Order,OrderLine


def find_all_orders():
    orders = Order.objects.all().order_by('moment')
    return orders


def find_all_orders_by_local(local):
    orders = Order.objects.all().filter(local=local)
    return orders


def find_order_line_by_order(order):
    orders_line = OrderLine.objects.all().filter(order_id=order)
    return orders_line


def set_order_line_status(order_line_id):
    order_line = OrderLine.objects.get(id=order_line_id)
    order_line.set_status(True)
    order_line.save()


def set_order_status(order_id):
    order = Order.objects.get(id=order_id)
    orders_line = OrderLine.objects.all().filter(order_id=order_id)

    # The order is completed if all order line are done
    if all(line.status is True for line in orders_line):
        order.set_status(True)
        order.save()

    # The order is doing if any order line is done
    elif any(line.status is True for line in orders_line):
        order.set_status(False)
        order.save()





