# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from bocatapp.models import User
from django.contrib.auth.models import Permission
from seller.models import Local
from administration.models import CreditCard



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

        customer = User(
            username='customer',
            email='customer@customer.com',
            first_name='customer')
        customer.set_password('customer')
        customer.save()
        customer.user_permissions.add(Permission.objects.get(codename="customer"))
        print('customer created...Ok')

        # ==============================================================================================================

        seller = User(
            username='seller',
            email='seller@seller.com',
            first_name='seller')
        seller.set_password('seller')
        seller.save()
        seller.user_permissions.add(Permission.objects.get(codename="seller"))

        print('Seller created...Ok')

        # ==============================================================================================================

        # local = Local(name='local1', description='local1Description', address='local1Address', phone=123456789,
        #               seller=seller)
        # # print (local.product_set)
        # local.save()
        # print ('Locals...Ok!')
        #
        # print ('Populated...Ok!')

        # ==============================================================================================================

        creditCard = CreditCard(
            holderName='customer',
            brandName='visa',
            expireMonth = '12',
            expireYear = '2020',
            cvv = '123',
            number = '4528348244106025',
            user=seller)

        creditCard.save()
        print('creditCard created...Ok')

        # ==============================================================================================================

    def handle(self, *args, **options):
        self._migrate()
