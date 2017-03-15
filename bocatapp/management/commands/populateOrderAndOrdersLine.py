# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from customer.models import Order, OrderLine

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _migrate(self):
        #Drop tables : Order-OrderLine
        print("Dropping tables")
        OrderLine.objects.all().delete()
        Order.objects.all().delete()
        print("Dropping tables OK")

        #Add Objects
        print("Creating Orders")
        order1 = Order(totalPrice=2.10, moment='2017-04-01 14:35:00',local="Rico-Rico",
                       comment="Sin salsas",customer="albcasmol",creditCard="12345689",
                       pickupMoment='2017-04-01 14:45:00')
        order1.save()

        order2 = Order(totalPrice=5.10, moment='2017-04-01 14:30:00', local="Pan-Sur",
                       comment="Mucho roquefort", customer="albcasmol", creditCard="12345689",
                       pickupMoment='2017-04-01 15:00:00')
        order2.save()

        order3 = Order(totalPrice=6.10, moment='2017-04-01 14:40:00', local="Ñan-Ñam",
                       comment="Lo quiero todo rapido", customer="albcasmol", creditCard="12345689",
                       pickupMoment='2017-04-01 14:55:00')
        order3.save()
        print("Orders OK")

        print("------------------------")
        print("Creating OrdersLine")

        order_line1 = OrderLine(quantity=1, name="Bocadillo de Pavo", price=2.10, order=order1)
        order_line1.save()

        order_line2 = OrderLine(quantity=1, name="Lomo con Roquefort", price=3.10, order=order2)
        order_line2.save()

        order_line3 = OrderLine(quantity=1, name="Donut chocolate", price=2.00, order=order2)
        order_line3.save()

        order_line4 = OrderLine(quantity=2, name="Bocadillo hipergigante", price=3.05, order=order3)
        order_line4.save()
        print("OrdersLine OK")

    def handle(self, *args, **options):
        self._migrate()
