from django.conf.urls import include, url

urlpatterns = [
    # Users URLs

    url(r'^creditcard/new/$', 'administration.views.creditcard_new', name='creditcard_new'),
    url(r'^creditcard$', 'administration.views.creditCard_list'),
    url(r'^creditcard/(?P<pk>[0-9]+)/$', 'administration.views.creditCard_detail'),

]
