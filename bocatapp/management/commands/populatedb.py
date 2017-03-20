# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from bocatapp.models import User
from django.contrib.auth.models import Permission
from seller.models import Local, Product
from customer.models import Order, CreditCard, OrderLine


# Los archivos que se encuentren en el paquete commands, se podr�n llamar
# desde manage.py, de forma que para popular la base de datos debemos hacer
# 'manage.py populate_db'

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _migrate(self):
        # Drop all tables
        print('Dropping tables...')

        User.objects.all().delete()

        print('Populating database...')

        # ==============================================================================================================

        admin_admin = User(
            username='admin',
            email='admin@admin.com',
            first_name='admin')
        admin_admin.set_password('admin')
        admin_admin.is_staff = True
        admin_admin.is_superuser = True
        admin_admin.save()
        print('Admin created...Ok')

        # ==============================================================================================================

        customer1 = User(
            username='customer1',
            email='customer1@customer1.com',
            first_name='customer1')
        customer1.set_password('customer1')
        customer1.save()
        customer1.user_permissions.add(Permission.objects.get(codename="customer"))

        customer2 = User(
            username='customer2',
            email='customer2@customer2.com',
            first_name='customer2')
        customer2.set_password('customer2')
        customer2.save()
        customer2.user_permissions.add(Permission.objects.get(codename="customer"))
        print('customer created...Ok')

        # ==============================================================================================================

        seller1 = User(
            username='seller1',
            email='seller1@seller1.com',
            first_name='seller1')
        seller1.set_password('seller1')
        seller1.save()
        seller1.user_permissions.add(Permission.objects.get(codename="seller"))

        seller2 = User(
            username='seller2',
            email='seller2@selle2r.com',
            first_name='seller2')
        seller2.set_password('seller2')
        seller2.save()
        seller2.user_permissions.add(Permission.objects.get(codename="seller"))

        print('Seller created...Ok')

        # ==============================================================================================================

        local1 = Local(name='local1', description='local1Description', address='local1Address', phone=123456789,
                       photo='www.photo.com', seller=seller1)

        local1.save()

        local2 = Local(name='local2', description='local2Description', address='local2Address', phone=123456789,
                       photo='www.photo.com', seller=seller2)

        local2.save()
        print ('Locals...Ok!')

        # ==============================================================================================================

        product1_local1 = Product(name='product1', price=1.5, local=local1)
        product1_local1.save()
        product2_local1 = Product(name='product2', price=1.0, local=local1)
        product2_local1.save()

        product1_local2 = Product(name='product1', price=1.0, local=local2)
        product1_local2.save()
        product2_local2 = Product(name='product2', price=2.5, local=local2)
        product2_local2.save()

        print ('Products...Ok!')

         # ==============================================================================================================
        
        creditCard = CreditCard(
            holderName='Paco Perez',
            brandName='visa',
            expireMonth = '12',
            expireYear = '2020',
            cvv = '123',
            number = '4528348244106025',
            user=customer1)
        creditCard.save()

        print('creditCard... Ok!')
        
         # ==============================================================================================================

        order1 = Order(totalPrice=2.10, moment='2017-04-01 14:35:00',local=local1,
                        comment="Sin salsas",customer=customer1,creditCard=creditCard,
                        pickupMoment='2017-04-01 14:45:00')
        order1.save()

        order2 = Order(totalPrice=5.10, moment='2017-04-01 14:30:00', local=local1,
                       comment="Mucho roquefort", customer=customer1, creditCard=creditCard,
                       pickupMoment='2017-04-01 15:00:00')
        order2.save()

        order3 = Order(totalPrice=6.10, moment='2017-04-01 14:40:00', local=local2,
                       comment="Lo quiero todo rapido", customer=customer2, creditCard=creditCard,
                       pickupMoment='2017-04-01 14:55:00')
        order3.save()
        print("Orders... Ok!")

         # ==============================================================================================================

        order_line1 = OrderLine(quantity=1, name="Bocadillo de Pavo", price=2.10, order=order1)
        order_line1.save()

        order_line2 = OrderLine(quantity=1, name="Lomo con Roquefort", price=3.10, order=order2)
        order_line2.save()

        order_line3 = OrderLine(quantity=1, name="Donut chocolate", price=2.00, order=order2)
        order_line3.save()

        order_line4 = OrderLine(quantity=2, name="Bocadillo hipergigante", price=3.05, order=order3)
        order_line4.save()

        print("OrdersLine... Ok!")


        print ('Populated...Ok!')

    def handle(self, *args, **options):
        self._migrate()
