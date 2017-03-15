# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from bocatapp.models import User
from django.contrib.auth.models import Permission


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

        print('Assesment...OK\n'
              'Populating database...OK\n'
              'Ready to use!')

        admin_admin = User(
            username='admin',
            email='admin@admin.com',
            first_name='admin')
        admin_admin.set_password('admin')
        admin_admin.is_staff = True
        admin_admin.is_superuser = True
        admin_admin.save()

        customer = User(
            username='customer',
            email='customer@customer.com',
            first_name='customer')
        customer.set_password('customer')
        customer.save()
        customer.user_permissions.add(Permission.objects.get(codename="customer"))

        print('Customer created...Ok')

    def handle(self, *args, **options):
        self._migrate()
