from django.conf.urls import include, url

urlpatterns = [
    # Users URLs

    url(r'^creditcard/new/$', 'administration.views.creditcard_new', name='creditCard_new'),
    url(r'^creditcard/$', 'administration.views.creditCard_list',name='creditCard_list'),
    url(r'^creditcard/delete/(?P<id1>[0-9]+)/$', 'administration.views.creditCard_delete',name='creditCard_delete'),

]
