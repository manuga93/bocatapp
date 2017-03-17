from django.conf.urls import include, url

urlpatterns = [
    # Users URLs
    url(r'^creditcard/new/$', 'administration.views.creditcard_new', name='creditcard_new'),
]
