from django.conf.urls import include, url
from bocatapp.decorators import permission_required

urlpatterns = [
    # Users URLs
    # url(r'^register$', RegistrationView.as_view(), name='guest_register')
    # url(r'^$', 'bocatapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^menu/(?P<pk>[0-9]+)/$', 'seller.views.menu_list', name="menu_list"),
    url(r'^local/$', 'seller.views.local_list'),
    url(r'^product/new/$', 'seller.views.product_new', name='product_new'),
    url(r'^product/list/(?P<pk>[0-9]+)/$', 'seller.views.product_list_category', name='product_list_category'),
    url(r'^category/new/$', 'seller.views.category_new', name='category_new'),
    url(r'^category/list/(?P<pk>[0-9]+)/$', 'seller.views.category_list', name='category_list'),
    url(r'^category/edit/(?P<pk>[0-9]+)/$', 'seller.views.category_edit', name='category_edit'),
    url(r'^local/new/$', 'seller.views.local_new', name='local_new'),
    url(r'^local/(?P<pk>[0-9]+)/$', 'seller.views.local_detail'),
    url(r'^local/(?P<pk>[0-9]+)/edit/$', 'seller.views.local_edit', name='local_edit'),
    url(r'^search/$', 'seller.views.search', name="search"),
    url(r'^local/getMine/(?P<pk>[0-9]+)$', 'seller.views.get_my_locals', name="locals_by_seller" ),
    url(r'^local/getOrders/(?P<pk>[0-9]+)$', 'seller.views.local_orders', name="local_orders")
]
