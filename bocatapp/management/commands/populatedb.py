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
        Allergen.objects.all().delete()

        print('Populating database...')

        # Admins =======================================================================================================

        admin_admin = User(
            username='admin',
            email='admin@admin.com',
            first_name='admin')
        admin_admin.set_password('@1b2c3d4')
        admin_admin.is_staff = True
        admin_admin.is_superuser = True
        admin_admin.save()
        admin_admin.user_permissions.remove(Permission.objects.get(codename="customer"))
        admin_admin.user_permissions.remove(Permission.objects.get(codename="seller"))

        print('Admin created...Ok')

        # Customers ====================================================================================================

        customer1 = User(
            username='julio44',
            email='julio44@customer.com',
            first_name='Julio', last_name='Parrales')
        customer1.set_password('@customer')
        customer1.save()
        customer1.user_permissions.add(Permission.objects.get(codename="customer"))

        customer2 = User(
            username='manuel',
            email='manuel@customer.com',
            first_name='Manuel')
        customer2.set_password('@customer')
        customer2.save()
        customer2.user_permissions.add(Permission.objects.get(codename="customer"))
        print('Customer created...Ok')

        # Sellers ======================================================================================================

        seller1 = User(
            username='jesusgar',
            email='jesus@seller.com',
            first_name='Jesus')
        seller1.set_password('@seller')
        seller1.save()
        seller1.user_permissions.add(Permission.objects.get(codename="seller"))

        seller2 = User(
            username='pomelo',
            email='pomelo@seller.com',
            first_name='pomelo')
        seller2.set_password('@seller')
        seller2.save()
        seller2.user_permissions.add(Permission.objects.get(codename="seller"))

        print('Seller created...Ok')

        # Locals =======================================================================================================

        namnam = Local(name=u'ÑamÑam',
                       description='Establecimiento espacialista en bocatas de pollo empañado y en cañas de chocolate',
                       address='Avd Reina Mercedes, 31, 41012 Sevilla', phone=697190794,postalCode="41012",
                       photo='https://s3-media1.fl.yelpcdn.com/bphoto/bqVR69LXKcTOh0imCBZt4A/ls.jpg', seller=seller1)

        namnam.save()

        ricorico = Local(name='Rico Rico', description='Tenemos las mejores ofertas para merendar!',
                         address='Av. de la Reina Mercedes, 39, 41012 Sevilla', phone=622397165, postalCode="41012",
                         photo='https://s3-media1.fl.yelpcdn.com/bphoto/QKiTaoNVWDuM1i-4Z3IJxA/168s.jpg',
                         seller=seller1)

        ricorico.save()

        cienm = Local(name='100 Montaditos', description='Los miercoles todo a 1€!',
                      address=' Av. de la Reina Mercedes, 43, 41012 Sevilla', phone=902197494,postalCode="41012",
                      photo='http://www.asesoresinmobiliariosbv.es/wp-content/uploads/2015/10/100-montaditos.jpg',
                      seller=seller2)

        cienm.save()
        print ('Locals...Ok!')

        # Categories =====================================================================================================

        especiales_namnam = Category(name='Especiales', description='Los bocatas más contundentes que encontrarás',
                                     local=namnam)
        especiales_namnam.save()

        vegetales_namnam = Category(name='Vegetales', description='Nuestros mejores bocadillos saludables',
                                    local=namnam)
        vegetales_namnam.save()

        bolleria_namnam = Category(name='Bollería', description='Todos nuestros surtido de dulces', local=namnam)
        bolleria_namnam.save()

        bolleria_ricorico = Category(name='Bollería', description='Todos nuestros surtido de dulces', local=ricorico)
        bolleria_ricorico.save()

        vegetales_ricorico = Category(name='Vegetales', description='Aquí nuestros productos sin carne', local=ricorico)
        vegetales_ricorico.save()

        especiales_ricorico = Category(name='Especiales', description='Los más grandes!', local=ricorico)
        especiales_ricorico.save()

        bebida1 = Category(name='Bebidas', description='Bebidas', local=ricorico)
        bebida1.save()
        bebida2 = Category(name='Bebidas', description='Bebidas', local=namnam)
        bebida2.save()
        bebida3 = Category(name='Bebidas', description='Bebidas', local=cienm)
        bebida3.save()
        print ('Categories...Ok!')

        # Allergens =====================================================================================================

        allergen1 = Allergen(name='Huevos', icon="http://icon-icons.com/icons2/463/PNG/128/Alergeno-Huevos_43897.png",
                             description='Contiene huevos')
        allergen1.save()

        allergen2 = Allergen(name='Gluten',
                             icon="http://icon-icons.com/icons2/463/PNG/128/Alergeno-cereal-con-gluten_43908.png",
                             description='Contiene gluten')
        allergen2.save()

        allergen3 = Allergen(name='Lacteos', icon="http://icon-icons.com/icons2/463/PNG/128/Alergeno-lacteos_43905.png",
                             description='Contiene lacteos o derivados')
        allergen3.save()

        allergen4 = Allergen(name='Frutos secos',
                             icon="http://icon-icons.com/icons2/463/PNG/128/Alergeno-frutos-secos_43906.png",
                             description='Contiene frutos secos')
        allergen4.save()

        allergen5 = Allergen(name='Sulfitos',
                             icon="http://icon-icons.com/icons2/463/PNG/128/Alergenos-sulfitos_43907.png",
                             description='Contiene sulfitos')
        allergen5.save()

        allergen6 = Allergen(name='Crustaceos',
                             icon="http://icon-icons.com/icons2/463/PNG/128/Alergeno-crustaceos_43903.png",
                             description='Contiene crustaceos')
        allergen6.save()

        allergen7 = Allergen(name='Pescado', icon="http://icon-icons.com/icons2/463/PNG/128/Alergeno-pescado_43898.png",
                             description='Contiene pescado')
        allergen7.save()

        allergen8 = Allergen(name='Moluscos',
                             icon="http://icon-icons.com/icons2/463/PNG/128/Alergeno-moluscos_43909.png",
                             description='Contiene Moluscos')
        allergen8.save()

        allergen9 = Allergen(name='Soja', icon="http://icon-icons.com/icons2/463/PNG/128/Alergeno-soja_43896.png",
                             description='Contiene soja')
        allergen9.save()

        allergen10 = Allergen(name='Sesamo', icon="http://icon-icons.com/icons2/463/PNG/128/Alergeno-sesamo_43899.png",
                              description='Contiene sesamo')
        allergen10.save()

        allergen11 = Allergen(name='Cacahuetes',
                              icon="http://icon-icons.com/icons2/463/PNG/128/Alergeno-cacahuetes_43904.png",
                              description='Contiene cacahuetes')
        allergen11.save()

        allergen12 = Allergen(name='Mostaza',
                              icon="http://icon-icons.com/icons2/463/PNG/128/alergeno_mostaza_43900.png",
                              description='Contiene mostaza')
        allergen12.save()

        allergen13 = Allergen(name='Apio', icon="http://icon-icons.com/icons2/463/PNG/128/Alergeno-apio_43902.png",
                              description='Contiene apio')
        allergen13.save()

        allergen14 = Allergen(name='Altramuz',
                              icon="http://icon-icons.com/icons2/463/PNG/128/Alergeno-altramuz_43901.png",
                              description='Contiene altramuz')
        allergen14.save()

        print ('Allergens...Ok!')

        # Products =====================================================================================================
        # RICORICO =====================================================================================================

        agua1 = Product(name='Agua', price=0.5, local=ricorico, ingredients="agua",
                        picture="https://www.tiptoprestaurantes.com/content/images/thumbs/0000184_agua-botella_480.png",
                        category=bebida1)
        agua1.save()

        cafe = Product(name='cafe', price=1.0, local=ricorico, ingredients="Café",
                       picture="http://estaticos.muyinteresante.es/uploads/images/article/55d31c013fafe8fa92bf40d6/cafe-colon_0.jpg",
                       category=bebida1)
        cafe.save()

        product1_ricorico = Product(name='59', price=2.0, local=ricorico,
                                    ingredients="Queso, lechuga, tomate, esparragos y salsa a elegir",
                                    picture="http://static.consumer.es/www/imgs/recetas/7/79014_g.jpg", category=especiales_ricorico)
        product1_ricorico.save()

        product2_ricorico = Product(name='60', price=2.6, local=ricorico,
                                    ingredients="Pechuga de pollo, beicon, queso, lechuga y salsa a elegir",
                                    picture="http://www.menshealth.es/rcs/articles/812/imagenes/139-bocadillo-pollo.jpg",
                                    category=especiales_ricorico)
        product2_ricorico.save()

        canachoco_ricorico = Product(name='caña de cholocate', price=1.0, local=ricorico,
                                     ingredients="chocolate, hojaldre y azúcar  glas",
                                     picture="http://pasteleriatiamaria.es/wp-content/uploads/2015/06/5153-Ca%C3%B1a-de-chocolate-Pasteleria-Tia-Maria.png",
                                     category=bolleria_ricorico)
        canachoco_ricorico.save()

        napolitana_ricorico = Product(name='Napolitana de cholocate', price=1.0, local=ricorico,
                                      ingredients="chocolate, hojaldre y virutas de chocolate",
                                      picture="http://www.panaderiapulido.com/sites/default/files/bolleria_napolitana.jpg",
                                      category=bolleria_ricorico)
        napolitana_ricorico.save()

        # ÑAMÑAM =====================================================================================================
        agua2 = Product(name='Agua', price=0.5, local=namnam, ingredients="agua",
                        picture="https://www.tiptoprestaurantes.com/content/images/thumbs/0000184_agua-botella_480.png",
                        category=bebida2)
        agua2.save()

        cocacola = Product(name='Cocacola', price=0.80, local=namnam, ingredients="Cocacola",
                           picture="https://www.corporativo.tia.com.ec/sites/almacenestia.com/files/productos/imagenescargadas/2014-10-18/247060.jpeg",
                           category=bebida2)
        cocacola.save()

        casa_namnam = Product(name='De la casa', price=2.10, local=namnam,
                              ingredients='Tortilla de patatas, lechuga, jamón serrano y mayonesa',
                              picture='https://img.over-blog-kiwi.com/1/39/41/41/20170404/ob_cf201c_1-018.jpg', category=especiales_namnam)
        casa_namnam.save()

        universitario_namnam = Product(name='Universitario', price=2.10, local=namnam,
                                       ingredients='Palitos de cangrejo, jamón york, lechuga y salsa rosa', category=especiales_namnam)
        universitario_namnam.save()

        canachoco_namnam = Product(name='caña de cholocate', price=1.0, local=namnam,
                                   ingredients="chocolate, hojaldre y azúcar  glas",
                                   picture="http://pasteleriatiamaria.es/wp-content/uploads/2015/06/5153-Ca%C3%B1a-de-chocolate-Pasteleria-Tia-Maria.png",
                                   category=bolleria_namnam)
        canachoco_namnam.save()

        napolitana_namnam = Product(name='Napolitana de cholocate', price=1.0, local=namnam,
                                    ingredients="chocolate, hojaldre y virutas de chocolate",
                                    picture="http://www.panaderiapulido.com/sites/default/files/bolleria_napolitana.jpg",
                                    category=bolleria_namnam)
        napolitana_namnam.save()

        # 100m =====================================================================================================

        cerveza = Product(name='Jarra de cerveza', price=1.5, local=cienm, ingredients="cebada, lúpulo",
                          picture="http://www.aceitedearganweb.com/wp-content/uploads/2015/10/cerveza.jpg"
                          ,category=bebida3)
        cerveza.save()

        print ('Products...Ok!')


        # Profiles =====================================================================================================

        profile_customer1 = Profile(user=customer1, phone=123456789, birth_date='1993-01-25',
                                    avatar='https://http2.mlstatic.com/mascara-v-de-venganza-pelicula-v-for-vendetta-D_NQ_NP_2613-MLM2719793745_052012-O.jpg')
        profile_customer1.save()

        profile_customer2 = Profile(user=customer2, phone=123456789, birth_date='1993-01-25')
        profile_customer2.save()

        profile_seller1 = Profile(user=seller1, phone=123456789, birth_date='1993-01-25')
        profile_seller1.save()

        profile_seller2 = Profile(user=seller2, phone=123456789, birth_date='1993-01-25')
        profile_seller2.save()

        print ('Profiles...Ok!')
        # CreditCard==============================================================================================================

        creditCard1 = CreditCard(
            holderName='Julio',
            brandName='visa',
            expireMonth='12',
            expireYear='2020',
            cvv='123',
            number='4528348244106025',
            user=customer1)
        creditCard1.save()

        creditCard2 = CreditCard(
            holderName='Jesus',
            brandName='visa',
            expireMonth='12',
            expireYear='2020',
            cvv='123',
            number='4528348244106025',
            user=seller1)

        creditCard2.save()
        print('creditCard created...Ok')

        print('creditCard... Ok!')

        # Order ==============================================================================================================

        order1 = Order(totalPrice=2.10, moment='2017-04-01 14:35:00', local=namnam,
                       comment="Sin salsas", customer=customer1, creditCard=creditCard1,
                       pickupMoment='2017-04-01 14:45:00', hour='14:45')
        order1.save()

        order2 = Order(totalPrice=3.30, moment='2017-04-01 14:30:00', local=ricorico,
                       comment="Mucho roquefort", customer=customer1, creditCard=creditCard1,
                       pickupMoment='2017-05-01 15:00:00', hour='15:00')
        order2.save()

        order3 = Order(totalPrice=6.10, moment='2017-04-01 14:40:00', local=ricorico,
                       comment="Frios por favor", customer=customer2, creditCard=creditCard2,
                       pickupMoment='2017-04-01 14:55:00', hour='14:55')
        order3.save()

        order4 = Order(totalPrice=6.70, moment='2017-04-01 15:45:00', local=namnam, customer=customer2,
                       creditCard=creditCard1, status=True, hour='15:45')
        order4.save()

        print("Orders... Ok!")

        # OrderLine==============================================================================================================

        order_line1 = OrderLine(quantity=1, name="De la casa", price=2.10, order=order1)
        order_line1.save()

        order_line2 = OrderLine(quantity=2, name="Caña de chocolate", price=2.20, order=order2)
        order_line2.save()

        order_line3 = OrderLine(quantity=1, name="Napolitana de chocolate", price=1.10, order=order2)
        order_line3.save()

        order_line4 = OrderLine(quantity=2, name="60", price=2.60, order=order3)
        order_line4.save()

        order_line5 = OrderLine(quantity=2, name="Universitario", price=2.10, order=order4)
        order_line5.save()

        print("OrdersLine... Ok!")


        # ==============================================================================================================

        shoppingCart1 = ShoppingCart(
            customer=customer1, checkout=False)

        shoppingCart1.save()

        shoppingCart2 = ShoppingCart(
            customer=customer2, checkout=False)

        shoppingCart2.save()
        print('ShoppingCart created...Ok')

        # ==============================================================================================================
        # Pack
        # ==============================================================================================================
        pack1 = Pack(name='Oferta diaria de la casa', price=2.5, endDate='2017-09-25', local=namnam)
        pack1.save()

        pack2 = Pack(name='Oferta diaria universitario', price=2.5, endDate='2017-09-25', local=namnam)
        pack2.save()

        pack3 = Pack(name='Oferta caña', price=1.5, endDate='2017-09-25', local=ricorico)
        pack3.save()

        pack4 = Pack(name='Oferta napolitana', price=1.5, endDate='2017-09-25', local=ricorico)
        pack4.save()

        print ('Packs...Ok!')

        # ==============================================================================================================
        # Product line
        # ==============================================================================================================
        product1_pack1 = ProductLine(quantity=1, product=casa_namnam, pack=pack1)
        product1_pack1.save()

        product2_pack1 = ProductLine(quantity=1, product=agua2, pack=pack1)
        product2_pack1.save()

        product1_pack2 = ProductLine(quantity=1, product=universitario_namnam, pack=pack2)
        product1_pack2.save()
        product2_pack2 = ProductLine(quantity=1, product=cocacola, pack=pack2)
        product2_pack2.save()

        product1_pack3 = ProductLine(quantity=1, product=cafe, pack=pack3)
        product1_pack3.save()
        product2_pack3 = ProductLine(quantity=1, product=canachoco_namnam, pack=pack3)
        product2_pack3.save()

        product1_pack4 = ProductLine(quantity=1, product=agua1, pack=pack4)
        product1_pack4.save()
        product2_pack4 = ProductLine(quantity=1, product=napolitana_ricorico, pack=pack4)
        product2_pack4.save()
        print ('Products line...Ok!')

        print ('Populated...Ok!')

        comment = Comment(
            description='Este local es de los peores que he visto en mi vida',
            rating='4',
            local = namnam,
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

        print('reports created...Ok')

        print ('Populated...Ok!')

        # ==============================================================================================================
    def handle(self, *args, **options):
        self._migrate()
