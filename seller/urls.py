from django.conf.urls import include, url

urlpatterns = [
    # Users URLs
    #url(r'^register$', RegistrationView.as_view(), name='guest_register')
    # url(r'^$', 'bocatapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^carta/$', 'seller.views.carta')
]
