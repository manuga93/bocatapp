# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from bocatapp.models import User
from django.contrib.auth.models import Permission
from seller.models import Local, Product, Pack, ProductLine, Local, Category, LocalCategory
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
        LocalCategory.objects.all().delete()

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
            first_name='Julio',
            last_name='Parrales',
            amount_money=10.0,
            phone=123454789,
            birth_date='1993-01-25',
            avatar='https://http2.mlstatic.com/mascara-v-de-venganza-pelicula-v-for-vendetta-D_NQ_NP_2613-MLM2719793745_052012-O.jpg')
        customer1.set_password('@customer')
        customer1.save()
        customer1.user_permissions.add(Permission.objects.get(codename="customer"))

        customer2 = User(
            username='manuel',
            email='manuel@customer.com',
            first_name='Manuel',
            last_name='GarriDev',
            amount_money=5.0,
            phone=123456889,
            birth_date='1993-01-25')
        customer2.set_password('@customer')
        customer2.save()
        customer2.user_permissions.add(Permission.objects.get(codename="customer"))

        customer3 = User(
            username='patri',
            email='patjimenez@customer.com',
            first_name='Patricia',
            last_name='Garcia',
            amount_money=15.0,
            phone=123456289,
            birth_date='1993-01-25')
        customer3.set_password('@customer')
        customer3.save()
        customer3.user_permissions.add(Permission.objects.get(codename="customer"))

        print('Customers created...Ok')

        # Sellers ======================================================================================================

        seller1 = User(
            username='jesusgar',
            email='jesus@seller.com',
            first_name='Jesus',
            last_name='Cabeza',
            phone=123456789,
            birth_date='1993-01-25')
        seller1.set_password('@seller')
        seller1.save()
        seller1.user_permissions.add(Permission.objects.get(codename="seller"))

        seller2 = User(
            username='pomelo',
            email='pomelo@seller.com',
            first_name='pomelo',
            last_name='pomeloide',
            phone=123456789,
            birth_date='1993-01-25')
        seller2.set_password('@seller')
        seller2.save()
        seller2.user_permissions.add(Permission.objects.get(codename="seller"))

        seller3 = User(
            username='franky',
            email='franky@gmail.com',
            first_name='Francisco',
            last_name='Pacheco',
            phone=123456789,
            birth_date='1987-06-14')
        seller3.set_password('franky987')
        seller3.save()
        seller3.user_permissions.add(Permission.objects.get(codename="seller"))

        seller4 = User(
            username='corchu',
            email='rafcorchuelo@seller.com',
            first_name='Rafael',
            last_name='Corchuelo',
            amount_money=15.0,
            phone=123456589,
            birth_date='1993-01-25')
        seller4.set_password('@seller')
        seller4.save()
        seller4.user_permissions.add(Permission.objects.get(codename="seller"))


        print('Sellers created...Ok')

        # Locals =======================================================================================================

        namnam = Local(name=u'ÑemÑem',
                       description='Establecimiento espacialista en bocatas de pollo empañado y en cañas de chocolate',
                       address='Avd Reina Mercedes, 31, 41012 Sevilla', phone=697190794, postalCode="41012",
                       photo='https://s3-media1.fl.yelpcdn.com/bphoto/bqVR69LXKcTOh0imCBZt4A/ls.jpg', seller=seller1,
                       avg_rating=4.00)
        namnam.save()

        ricorico = Local(name='Rica Rica', description='Tenemos las mejores ofertas para merendar!',
                         address='Av. de la Reina Mercedes, 39, 41012 Sevilla', phone=622397165, postalCode="41012",
                         photo='https://s3-media1.fl.yelpcdn.com/bphoto/QKiTaoNVWDuM1i-4Z3IJxA/168s.jpg',
                         seller=seller1, avg_rating=4.00)
        ricorico.save()

        cienm = Local(name='1000 Montaditos', description='Los miercoles todo a 1€!',
                      address=' Av. de la Reina Mercedes, 43, 41012 Sevilla', phone=902197494, postalCode="41012",
                      photo='http://www.asesoresinmobiliariosbv.es/wp-content/uploads/2015/10/100-montaditos.jpg',
                      seller=seller2, avg_rating=3.50)

        cienm.save()

        frankyb = Local(name='Bocatería Frankys', description='¿Quieres un Bocata? Pues ven a comerte el mejor!',
                        address=' Av. de la Reina Mercedes, 45, 41012 Sevilla', phone=902197494, postalCode="41012",
                        photo='http://fotos.subefotos.com/7b9bc1c91b4ba708f179ee6d79d2ac6fo.jpg',
                        seller=seller3, avg_rating=5)
        frankyb.save()

        buenProvecho = Local(name='Buen provecho', description='Comida casera hecha con todo el cariño del mundo',
                             address='Calle Monzon, 24,41012 Sevilla', phone=902197494, postalCode="41012",
                             photo='http://ultrarradio.com/wp-content/uploads/2013/04/c_caseras1.jpg',
                             seller =seller2, avg_rating=4.00)
        buenProvecho.save()


        print ('Locals...Ok!')

        # Super Categories =============================================================================================

        supercat_bocadillos = LocalCategory(name="Bocadillos/Sandwiches")
        supercat_bocadillos.save()
        supercat_bocadillos.locals.add(namnam, ricorico, cienm, frankyb, buenProvecho)
        supercat_bocadillos.save()

        supercat_pizza = LocalCategory(name="Pizzas")
        supercat_pizza.save()
        supercat_pizza.locals.add(frankyb)
        supercat_pizza.save()

        supercat_pasta = LocalCategory(name="Pasta")
        supercat_pasta.save()
        supercat_pasta.locals.add(buenProvecho, frankyb, namnam)
        supercat_pasta.save()


        supercat_kebab = LocalCategory(name="Kebab")
        supercat_kebab.save()
        supercat_kebab.locals.add(namnam, ricorico)
        supercat_kebab.save()

        supercat_bolleria = LocalCategory(name="Bolleria")
        supercat_bolleria.save()
        supercat_bolleria.locals.add(ricorico, namnam, cienm, frankyb)
        supercat_bolleria.save()

        print("Super categories created...Ok")

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

        bocadillos_frank = Category(name='Bocadillos', description='', local=frankyb)
        bocadillos_frank.save()

        bocapizza_frank = Category(name='BocaPizza', description='', local=frankyb)
        bocapizza_frank.save()

        bolleria_frank = Category(name='Bollería', description='', local=frankyb)
        bolleria_frank.save()

        bebidas_frank = Category(name='Bebidas', description='', local=frankyb)
        bebidas_frank.save()

        platos_calientes_buenProvecho = Category(name='Platos calientes', description='', local=buenProvecho)
        platos_calientes_buenProvecho.save()

        platos_frios_buenProvecho = Category(name='Platos frios', description='', local=buenProvecho)
        platos_frios_buenProvecho.save()

        bebidas_buenProvecho = Category(name='Bebidas', description='', local=buenProvecho)
        bebidas_buenProvecho.save()


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
        # Bocateria Franky's ===========================================================================================
        #  bocadillos_frank bocapizza_frank bolleria_frank bebidas_frank
        cochinito = Product(name='Cochinito', price=1, local=frankyb, ingredients="Cochinito",
                            category=bocadillos_frank)

        cochinito.save()

        tortilla = Product(name='Tortilla', price=1, local=frankyb, ingredients="Tortilla",
                           category=bocadillos_frank)

        tortilla.save()

        jamon_serrano = Product(name='Jamón Serrano', price=1.5, local=frankyb, ingredients="Jamón Serrano",
                                category=bocadillos_frank)
        jamon_serrano.save()

        bocapizza1 = Product(name='El 1', price=1.5, local=frankyb, ingredients="Tomate + Queso + Bacon + Cochinito",
                             category=bocapizza_frank)
        bocapizza1.save()

        bocapizza2 = Product(name='El 2', price=1.5, local=frankyb, ingredients="Tomate + Queso + Bacon + Salchicha",
                             category=bocapizza_frank)
        bocapizza2.save()

        palmerafr = Product(name='Palmera Casera', price=1.1, local=frankyb, ingredients="Palmera de Huevo",
                            category=bolleria_frank)
        palmerafr.save()

        palmerachocofr = Product(name='Palmera Morenita', price=1.1, local=frankyb, ingredients="Palmera de Chocolate",
                                 category=bolleria_frank)
        palmerachocofr.save()

        aguafr = Product(name='Agua', price=0.8, local=frankyb, ingredients="Agua",
                         category=bebidas_frank)
        aguafr.save()

        fantalimonfr = Product(name='Fanta Naranja', price=0.8, local=frankyb, ingredients="Fanta Naranja",
                               category=bebidas_frank)
        fantalimonfr.save()

        fantanaranjafr = Product(name='Fanta Limón', price=0.8, local=frankyb, ingredients="Fanta Limón",
                                 category=bebidas_frank)
        fantanaranjafr.save()

        # RICORICO =====================================================================================================

        agua1 = Product(name='Agua', price=0.5, local=ricorico, ingredients="agua",
                        category=bebida1)
        agua1.save()

        cafe = Product(name='cafe', price=1.0, local=ricorico, ingredients="Café",
                       category=bebida1)
        cafe.save()

        product1_ricorico = Product(name='59', price=2.0, local=ricorico,
                                    ingredients="Queso, lechuga, tomate, esparragos y salsa a elegir",
                                    category=especiales_ricorico)
        product1_ricorico.save()

        product2_ricorico = Product(name='60', price=2.6, local=ricorico,
                                    ingredients="Pechuga de pollo, beicon, queso, lechuga y salsa a elegir",
                                    category=especiales_ricorico)
        product2_ricorico.save()

        canachoco_ricorico = Product(name='caña de cholocate', price=1.0, local=ricorico,
                                     ingredients="chocolate, hojaldre y azúcar  glas",
                                     category=bolleria_ricorico)
        canachoco_ricorico.save()

        napolitana_ricorico = Product(name='Napolitana de cholocate', price=1.0, local=ricorico,
                                      ingredients="chocolate, hojaldre y virutas de chocolate",
                                      category=bolleria_ricorico)
        napolitana_ricorico.save()

        # ÑAMÑAM =====================================================================================================
        agua2 = Product(name='Agua', price=0.5, local=namnam, ingredients="agua",
                        category=bebida2)
        agua2.save()

        cocacola = Product(name='Cocacola', price=0.80, local=namnam, ingredients="Cocacola",
                           category=bebida2)
        cocacola.save()

        casa_namnam = Product(name='De la casa', price=2.10, local=namnam,
                              ingredients='Tortilla de patatas, lechuga, jamón serrano y mayonesa',
                              category=especiales_namnam)
        casa_namnam.save()

        universitario_namnam = Product(name='Universitario', price=2.10, local=namnam,
                                       ingredients='Palitos de cangrejo, jamón york, lechuga y salsa rosa',
                                       category=especiales_namnam)
        universitario_namnam.save()

        canachoco_namnam = Product(name='caña de cholocate', price=1.0, local=namnam,
                                   ingredients="chocolate, hojaldre y azúcar  glas",
                                   category=bolleria_namnam)
        canachoco_namnam.save()

        napolitana_namnam = Product(name='Napolitana de cholocate', price=1.0, local=namnam,
                                    ingredients="chocolate, hojaldre y virutas de chocolate",
                                    category=bolleria_namnam)
        donutOreo_namnam = Product(name='Donut de oreo', price=1.0, local=namnam, ingredients='donut,oreo,nata',
                                    category=bolleria_namnam)
        donutOreo_namnam.save()
        napolitana_namnam.save()

        # 100m =====================================================================================================

        cerveza = Product(name='Jarra de cerveza', price=1.5, local=cienm, ingredients="cebada, lúpulo",
                            category=bebida3)
        cerveza.save()

        # Buen Provecho ================================================================================================
        paella = Product(name='Paella(200gr)', price='2.5', local=buenProvecho, ingredients='arroz, pollo, colorante, sofrito',
                         category=platos_calientes_buenProvecho)
        paella.save()

        fabada = Product(name='Fabada asturiana(200gr)', price='2.5', local=buenProvecho, ingredients='alubias, chorizo, morcilla',
                         category=platos_calientes_buenProvecho)
        fabada.save()

        croquetas = Product(name='Croquetas de puchero(200gr)', price=2.5, local=buenProvecho,
                            ingredients='bechamel, pringa de puchero, pan rallado',
                            category=platos_calientes_buenProvecho)
        croquetas.save()

        tortilla_patatas = Product(name='Tortilla de patata (250gr)', price=4, local=buenProvecho,
                                   ingredients='huevo, patata, cebolla',
                                   category=platos_calientes_buenProvecho)
        tortilla_patatas.save()

        ensaladilla_rusa = Product(name='Ensaladilla rusa(200gr)', price=2.0, local=buenProvecho,
                                   ingredients='huevo, mahonesa, aceitunas, atun',
                                   category=platos_frios_buenProvecho)
        ensaladilla_rusa.save()

        patatas_alioli = Product(name='Patatas con alioli(200gr)', price=2.0 ,local=buenProvecho,
                                 ingredients='patatas, alioli',
                                 category=platos_frios_buenProvecho)
        patatas_alioli.save()

        aguabp = Product(name='Agua', price=0.6, local=buenProvecho, ingredients="Agua", category=bebidas_buenProvecho)
        aguabp.save()

        cokebp = Product(name='Coca-cola', price=1.0, local=buenProvecho, ingredients='Coca-cola',
                         category=bebidas_buenProvecho)
        cokebp.save()

        fantaNaranja = Product(name='Fanta Naranja', price=1.0, local=buenProvecho,ingredients='Fanta naranja'
                               ,category=bebidas_buenProvecho)
        fantaNaranja.save()

        fantaLimon = Product(name='Fanta Limon', price=1.0, local=buenProvecho, ingredients='Fanta limon',
                              category=bebidas_buenProvecho)
        fantaLimon.save()

        print ('Products...Ok!')

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

        creditCard3 = CreditCard(
            holderName='R.Corchuelo',
            brandName='Visa',
            expireMonth='08',
            expireYear='2020',
            cvv='255',
            number='4361744206052381',
            user=seller4)

        creditCard3.save()

        creditCard4 = CreditCard(
            holderName='P.Jimenez',
            brandName='Visa',
            expireMonth='11',
            expireYear='2021',
            cvv='142',
            number='4882910476013938',
            user=customer3)

        creditCard4.save()


        print('creditCard created...Ok')

        print('creditCard... Ok!')

        # Order ==============================================================================================================

        order1 = Order(totalPrice=2.10, moment='2017-04-01 14:35:00', local=namnam,
                       comment="Sin salsas", customer=customer1, creditCard=creditCard1,
                       pickupMoment='2017-04-01 14:45:00')
        order1.save()

        order2 = Order(totalPrice=3.30, moment='2017-04-01 14:30:00', local=ricorico,
                       comment="Mucho roquefort", customer=customer1, creditCard=creditCard1,
                       pickupMoment='2017-05-01 15:00:00')
        order2.save()

        order3 = Order(totalPrice=6.10, moment='2017-04-01 14:40:00', local=ricorico,
                       comment="Frios por favor", customer=customer2, creditCard=creditCard2,
                       pickupMoment='2017-04-01 14:55:00')
        order3.save()

        order4 = Order(totalPrice=6.70, moment='2017-05-11 15:45:00', local=namnam, customer=customer2,
                       creditCard=creditCard1, status=False, pickupMoment='2017-05-31 14:00:00')
        order4.save()

        order5 = Order(totalPrice=9.50, moment='2017-04-27 14:45:00', local=frankyb, customer=customer3,
                       creditCard=creditCard3, status=True, pickupMoment='2017-05-27 15:10:00')
        order5.save()

        order6 = Order(totalPrice=5.30, moment='2017-04-27 13:45:00',local=frankyb, customer=customer1,
                       creditCard=creditCard3, status=True, pickupMoment='2017-06-02 15:35:00')
        order6.save()

        order7 = Order(totalPrice=5.30, moment='2017-05-15 13:45:00', local=frankyb,customer=customer2,
                       creditCard=creditCard4, status=False, pickupMoment='2017-05-24 14:45:00')
        order7.save()

        order8 = Order(totalPrice=10.50, moment='2017-05-15 14:15:00', local=buenProvecho,customer=customer3,
                       creditCard=creditCard3,status=False, pickupMoment='2017-05-25 13:10:00')
        order8.save()

        order9 = Order(totalPrice=8.80, moment='2017-05-15 14:00', local=frankyb, customer=customer3,
                       creditCard=creditCard4, status=False, pickupMoment='2017-05-26 16:30:00')
        order9.save()



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

        order_line_order5_1 = OrderLine(quantity=2, name='Cochinito', price=1.0 , order=order5)

        order_line_order5_2 = OrderLine(quantity=3, name='Tortilla', price=1.0, order=order5)

        order_line_order5_3 = OrderLine(quantity=3, name='Jamon serrano', price=1.50, order=order5)

        order_line_order5_1.save()
        order_line_order5_2.save()
        order_line_order5_3.save()

        order_line_order6_1 = OrderLine(quantity=3, name='Jamon serrano', price=1.50, order=order6)
        order_line_order6_2 = OrderLine(quantity=1, name='Agua', price=0.80, order=order6)

        order_line_order6_1.save()
        order_line_order6_2.save()

        order_line_order7_1 = OrderLine(quantity=1, name='Agua', price=0.50, order=order7)
        order_line_order7_2 = OrderLine(quantity=3, name='El 2', price=1.50, order=order7)

        order_line_order7_1.save()
        order_line_order7_2.save()

        order_line_order8_1 = OrderLine(quantity=1, name='Tortilla patatas', price=4.0, order=order8)
        order_line_order8_2 = OrderLine(quantity=2, name='Ensaladilla rusa', price=2.0, order=order8)
        order_line_order8_3 = OrderLine(quantity=1, name='Patatas con alioli', price=2.0, order=order8)

        order_line_order8_1.save()
        order_line_order8_2.save()
        order_line_order8_3.save()

        order_line_order9_1 = OrderLine(quantity=2, name='El 1', price=1.5, order=order9)
        order_line_order9_2 = OrderLine(quantity=2, name='El 2', price=1.5, order=order9)
        order_line_order9_3 = OrderLine(quantity=2, name='Cochinito', price=1.0, order=order9)
        order_line_order9_4 = OrderLine(quantity=1, name='Agua', price=0.8, order=order9)

        order_line_order9_1.save()
        order_line_order9_2.save()
        order_line_order9_3.save()
        order_line_order9_4.save()




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

        comment1 = Comment(
            description='Todo rapido y perfecto',
            rating='5',
            local=frankyb,
            reported=0,
            customer=customer1)

        comment1.save()

        comment2 = Comment(
            description='No esta mal, aunque mucha verdura y poco pollo',
            rating='3',
            local=namnam,
            reported=0,
            customer=customer2)

        comment2.save()

        comment3 = Comment(
            description='Me encanta, el ñem-ñem no falla!',
            rating='5',
            local=namnam,
            reported=0,
            customer=customer1)

        comment3.save()

        comment4 = Comment(
            description='Siempre entra una cerveza mas!',
            rating='5',
            local=cienm,
            reported=0,
            customer=customer1)

        comment4.save()

        comment5 = Comment(
            description='Echamos de menos los miercoles la cerveza a un euro!',
            rating='2',
            local=cienm,
            reported=0,
            customer=customer2)

        comment5.save()

        comment6 = Comment(
            description='Los mejores bocapizzas de RM, un saludito pa el Dani!',
            rating='5',
            local=frankyb,
            reported=0,
            customer=customer2)

        comment6.save()

        comment7 = Comment(
            description='Rica Rica siempre en nuestros corazones, pero con la caña+batido 0,80 molabais mas que con los papelitos',
            rating='4',
            local=ricorico,
            reported=0,
            customer=customer2)

        comment7.save()

        comment8 = Comment(
            description='Comida muy de muy buena calidad!!',
            rating='4',
            local=buenProvecho,
            reported=0,
            customer=customer2)

        comment8.save()

        comment9 = Comment(
            description='La tortilla de patata tremenda!!!',
            rating='4',
            local=buenProvecho,
            reported=0,
            customer=customer1)

        comment9.save()






        print('comments created...Ok')

        report1 = Report(
            reason='Este comentario no tiene fundamento',
            accepted=0,
            decline=0,
            comment=comment1,
            customer=customer2)

        report1.save()

        report2 = Report(
            reason='Este comentario no me gusta',
            accepted=0,
            decline=0,
            comment=comment2,
            customer=customer2)

        report2.save()

        report3 = Report(
            reason='Este comentario es insultante',
            accepted=0,
            decline=0,
            comment=comment1,
            customer=customer2)

        report3.save()

        print('reports created...Ok')

        print ('Populated...Ok!')

        # ==============================================================================================================
        print ('POPULATE FINISH')

    def handle(self, *args, **options):
        self._migrate()
