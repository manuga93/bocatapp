# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from bocatapp.models import User, Profile
from django.contrib.auth.models import Permission
from seller.models import Local, Product, Pack, ProductLine, Local, Category
from customer.models import Order, CreditCard, OrderLine, ShoppingCart, Comment, Report
from administration.models import CreditCard, Allergen


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
        Product.objects.all().delete()
        CreditCard.objects.all().delete()
        Order.objects.all().delete()
        OrderLine.objects.all().delete()
        Local.objects.all().delete()
        CreditCard.objects.all().delete()
        Pack.objects.all().delete()
        ProductLine.objects.all().delete()
        Category.objects.all().delete()

        print('Populating database...')

        # Admins =======================================================================================================

        admin_admin = User(
            username='admin',
            email='admin@admin.com',
            first_name='admin')
        admin_admin.set_password('admin')
        admin_admin.is_staff = True
        admin_admin.is_superuser = True
        admin_admin.save()
        print('Admin created...Ok')

        # Customers ====================================================================================================

        customer1 = User(
            username='customer1',
            email='customer1@customer1.com',
            first_name='customer1Firstname', last_name='customer1Lastname')
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
        print('Customer created...Ok')

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

        local1 = Local(name='local1', description='local1Description', address='local1Address', phone=123456789, seller=seller1)

        local1.save()

        local2 = Local(name='local2', description='local2Description', address='local2Address', phone=123456789, seller=seller2)

        local2.save()
        print ('Locals...Ok!')

        # Categories =====================================================================================================

        category1_local1 = Category(name='Category 1', description='Description of Category 1', local=local1)
        category1_local1.save()

        category2_local1 = Category(name='Category 2', description='Description of Category 2', local=local1)
        category2_local1.save()

        category3_local1 = Category(name='Category 3', description='Description of Category 3', local=local1)
        category3_local1.save()

        category1_local2 = Category(name='Category 1', description='Description of Category 1', local=local2)
        category1_local2.save()

        print ('Categories...Ok!')

        # Allergens =====================================================================================================

        allergen1 = Allergen(name='Huevos', icon="http://icon-icons.com/icons2/463/PNG/128/Alergeno-Huevos_43897.png", description='Contiene huevos')
        allergen1.save()

        allergen2 = Allergen(name='Gluten', icon="http://icon-icons.com/icons2/463/PNG/128/Alergeno-cereal-con-gluten_43908.png", description='Contiene gluten')
        allergen2.save()

        allergen3 = Allergen(name='Lacteos', icon="http://icon-icons.com/icons2/463/PNG/128/Alergeno-lacteos_43905.png", description='Contiene lacteos o derivados')
        allergen3.save()

        allergen4 = Allergen(name='Frutos secos', icon="http://icon-icons.com/icons2/463/PNG/128/Alergeno-frutos-secos_43906.png", description='Contiene frutos secos')
        allergen4.save()

        allergen5 = Allergen(name='Sulfitos', icon="http://icon-icons.com/icons2/463/PNG/128/Alergenos-sulfitos_43907.png", description='Contiene sulfitos')
        allergen5.save()

        allergen6 = Allergen(name='Crustaceos', icon="http://icon-icons.com/icons2/463/PNG/128/Alergeno-crustaceos_43903.png", description='Contiene crustaceos')
        allergen6.save()

        allergen7 = Allergen(name='Pescado', icon="http://icon-icons.com/icons2/463/PNG/128/Alergeno-pescado_43898.png", description='Contiene pescado')
        allergen7.save()

        allergen8 = Allergen(name='Moluscos', icon="http://icon-icons.com/icons2/463/PNG/128/Alergeno-moluscos_43909.png", description='Contiene Moluscos')
        allergen8.save()

        allergen9 = Allergen(name='Soja', icon="http://icon-icons.com/icons2/463/PNG/128/Alergeno-soja_43896.png", description='Contiene soja')
        allergen9.save()

        allergen10 = Allergen(name='Sesamo', icon="http://icon-icons.com/icons2/463/PNG/128/Alergeno-sesamo_43899.png", description='Contiene sesamo')
        allergen10.save()

        allergen11 = Allergen(name='Cacahuetes', icon="http://icon-icons.com/icons2/463/PNG/128/Alergeno-cacahuetes_43904.png", description='Contiene cacahuetes')
        allergen11.save()

        allergen12 = Allergen(name='Mostaza', icon="http://icon-icons.com/icons2/463/PNG/128/alergeno_mostaza_43900.png", description='Contiene mostaza')
        allergen12.save()

        allergen13 = Allergen(name='Apio', icon="http://icon-icons.com/icons2/463/PNG/128/Alergeno-apio_43902.png", description='Contiene apio')
        allergen13.save()

        allergen14 = Allergen(name='Altramuz', icon="http://icon-icons.com/icons2/463/PNG/128/Alergeno-altramuz_43901.png", description='Contiene altramuz')
        allergen14.save()

        print ('Allergens...Ok!')

        # Products =====================================================================================================

        product1_local1 = Product(name='product1', price=1.5, local=local1, ingredients="Lentejas, garbanzos y lechuga", picture="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Bocadillo_Espa%C3%B1ol.jpg/240px-Bocadillo_Espa%C3%B1ol.jpg")
        product1_local1.save()
        product1_local1.category.add(category1_local1, category2_local1)
        product1_local1.save()

        product2_local1 = Product(name='product2', price=1.0, local=local1, ingredients="Lentejas, garbanzos y tomate", picture="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Bocadillo_Espa%C3%B1ol.jpg/240px-Bocadillo_Espa%C3%B1ol.jpg")
        product2_local1.save()

        product3_local1 = Product(name='product3', price=1.0, local=local1)
        product3_local1.save()

        product4_local1 = Product(name='product4', price=1.0, local=local1)
        product4_local1.save()

        product1_local2 = Product(name='product1', price=1.0, local=local2, ingredients="Lentejas, cominio y mayonesa", picture="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Bocadillo_Espa%C3%B1ol.jpg/240px-Bocadillo_Espa%C3%B1ol.jpg")
        product1_local2.save()

        product2_local2 = Product(name='product2', price=2.5, local=local2, ingredients="Ketchup, mostaza y mojo picon", picture="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Bocadillo_Espa%C3%B1ol.jpg/240px-Bocadillo_Espa%C3%B1ol.jpg")
        product2_local2.save()

        product2_local2.category.add(category1_local2)
        product2_local2.save()

        product3_local2 = Product(name='product3', price=1.0, local=local2)
        product3_local2.save()

        product4_local2 = Product(name='product4', price=1.0, local=local2)
        product4_local2.save()

        print ('Products...Ok!')



        # ==============================================================================================================

        creditCard = CreditCard(
            holderName='customer',
            brandName='visa',
            expireMonth='12',
            expireYear='2020',
            cvv='123',
            number='4528348244106025',
            user=seller1)

        creditCard.save()
        print('CreditCard created...Ok')

        # ==============================================================================================================

        shoppingCart1 = ShoppingCart(
            customer=customer1)

        shoppingCart1.save()

        shoppingCart2 = ShoppingCart(
            customer=customer2)

        shoppingCart2.save()
        print('ShoppingCart created...Ok')

        # ==============================================================================================================
        # Pack
        # ==============================================================================================================
        pack1 = Pack(name='Pack 1', price=3.5, endDate='2017-04-25', local=local1)
        pack1.save()

        pack2 = Pack(name='Pack 2', price=1.5, endDate='2017-09-25', local=local1)
        pack2.save()

        pack3 = Pack(name='Pack 3', price=5.0, endDate='2017-09-25', local=local1)
        pack3.save()

        print ('Packs...Ok!')

        # ==============================================================================================================
        # Product line
        # ==============================================================================================================
        product1_pack1 = ProductLine(quantity=2, product=product1_local1, pack=pack1)
        product1_pack1.save()

        product2_pack1 = ProductLine(quantity=2, product=product2_local1, pack=pack1)
        product2_pack1.save()

        product3_pack1 = ProductLine(quantity=1, product=product3_local1, pack=pack1)
        product3_pack1.save()

        product1_pack2 = ProductLine(quantity=1, product=product1_local1, pack=pack2)
        product1_pack2.save()
        product2_pack2 = ProductLine(quantity=1, product=product2_local1, pack=pack2)
        product2_pack2.save()
        product3_pack2 = ProductLine(quantity=1, product=product2_local1, pack=pack2)
        product3_pack2.save()

        product3_pack3 = ProductLine(quantity=1, product=product3_local1, pack=pack3)
        product3_pack3.save()
        product4_pack3 = ProductLine(quantity=1, product=product3_local1, pack=pack3)
        product4_pack3.save()
        print ('Products line...Ok!')

        print ('Populated...Ok!')

        comment = Comment(
            description='Este local es de los peores que he visto en mi vida',
            rating='4',
            local = local1,
            reported=0,
            customer=customer1)

        comment.save()
        print('comments created...Ok')

        report1 = Report(
            reason='Este comentario no tiene fundamento',
            accepted=0,
            decline=0,
            comment=comment)

        report1.save()



        report4.save()
        print('reports created...Ok')

        print ('Populated...Ok!')

        # ==============================================================================================================
    def handle(self, *args, **options):
        self._migrate()
