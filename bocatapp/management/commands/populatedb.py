# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from bocatapp.models import User, Profile
from django.contrib.auth.models import Permission
from seller.models import Local, Product


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

        # Admins =======================================================================================================

        admin_admin = User(
            username='admin',
            email='admin@admin.com',
            first_name='admin')
        admin_admin.set_password('admin')
        admin_admin.is_staff = True
        admin_admin.is_superuser = True
        self.save = admin_admin.save()
        print('Admin created...Ok')

        # Customers ====================================================================================================

        customer1 = User(
            username='customer1',
            email='customer1@customer1.com',
            first_name='customer1Firstname',last_name='customer1Lastname')
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

        # Sellers ======================================================================================================

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

        # Locals =======================================================================================================

        local1 = Local(name='local1', description='local1Description', address='local1Address', phone=123456789,
                       photo='www.photo.com', seller=seller1)

        local1.save()

        local2 = Local(name='local2', description='local2Description', address='local2Address', phone=123456789,
                       photo='www.photo.com', seller=seller2)

        local2.save()
        print ('Locals...Ok!')

        # Products =====================================================================================================

        product1_local1 = Product(name='product1', price=1.5, local=local1)
        product1_local1.save()
        product2_local1 = Product(name='product2', price=1.0, local=local1)
        product2_local1.save()

        product1_local2 = Product(name='product1', price=1.0, local=local2)
        product1_local2.save()
        product2_local2 = Product(name='product2', price=2.5, local=local2)
        product2_local2.save()

        print ('Products...Ok!')

        # Profiles =====================================================================================================

        # user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
        # phone = models.CharField(max_length=14)
        # birth_date = models.DateField(null=True, blank=True) YYYY-MM-DD
        # avatar = models.URLField(default=default)
        profile_customer1 = Profile(user=customer1, phone=123456789, birth_date='1993-01-25')
        profile_customer1.save()

        profile_customer2 = Profile(user=customer2, phone=123456789, birth_date='1993-01-25')
        profile_customer2.save()

        profile_seller1 = Profile(user=seller1, phone=123456789, birth_date='1993-01-25')
        profile_seller1.save()

        profile_seller2 = Profile(user=seller2, phone=123456789, birth_date='1993-01-25')
        profile_seller2.save()

        print ('Profiles...Ok!')
        print ('Populated...Ok!')

    def handle(self, *args, **options):
        self._migrate()
