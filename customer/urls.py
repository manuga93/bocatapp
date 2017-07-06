from django.conf.urls import include, url

urlpatterns = [
    # Users URLs
    # url(r'^register$', RegistrationView.as_view(), name='guest_register')
    url(r'^orders/$', 'customer.views.orders_by_customer'),
    url(r'^comment/(?P<pk>[0-9]+)/$', 'customer.views.comment_new', name="comment_new"),
    url(r'^comments/(?P<pk>[0-9]+)/$', 'customer.views.comment_list', name="comment_list"),
    url(r'^report/(?P<pk>[0-9]+)/$', 'customer.views.report_new', name="report_new"),
    url(r'^reports/$', 'customer.views.report_list', name="report_list"),
    url(r'^report/accept/(?P<pk>[0-9]+)/$', 'customer.views.report_accept', name="report_accept"),
    url(r'^report/decline/(?P<pk>[0-9]+)/$', 'customer.views.report_decline', name="report_decline"),
    url(r'^orders/$', 'customer.views.orders_by_customer', name="orders_by_customer"),
    url(r'^cancelOrder/(?P<pk>[0-9]+)/$', 'customer.views.cancel_order', name="cancel_order"),
    url(r'^checkout/(?P<pk>[0-9]+)/$', 'customer.views.checkout', name="checkout"),
    url(r'^checkout/save/$', 'customer.views.do_checkout', name="do_checkout"),
    url(r'^search/(?P<local_id>[0-9]+)/$', 'customer.views.search_product', name="search_product"),
    url(r'^recharge/$', 'customer.views.recharge_account', name="recharge_account"),
    url(r'^recharge/success/$', 'customer.views.recharge_account_success', name="recharge_account_success"),
    url(r'^recharge/failure/$', 'customer.views.recharge_account_failure', name="recharge_account_failure"),
    url(r'^recharge/notification/$', 'customer.views.recharge_account_notification', name="recharge_account_notification"),

]
