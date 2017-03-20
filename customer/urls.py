from django.conf.urls import include, url

urlpatterns = [
    # Users URLs
    # url(r'^register$', RegistrationView.as_view(), name='guest_register')
    url(r'^orders/$', 'customer.views.all_orders'),
    url(r'^ordersLine/(?P<order_id>[0-9]+)/$', 'customer.views.order_line_by_order'),
    url(r'^do_order_line/(?P<id1>[0-9]+)/$', 'customer.views.do_order_line'),
    url(r'^orders/(?P<pk>[0-9]+)/$', 'customer.views.orders_by_customer', name="orders_by_customer")

]
