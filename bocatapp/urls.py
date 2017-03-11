from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^signup/$', views.signup),
    url(r'^admin/', admin.site.urls),
    url(r'^seller/', include('seller.urls')),
    url(r'^administration/', include('administration.urls')),
    url(r'^customer/', include('customer.urls'))
]
