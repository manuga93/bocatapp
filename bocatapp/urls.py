from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'bocatapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    
    url(r'^admin/', admin.site.urls),
    url(r'^/seller', include('seller.urls')),
    url(r'^administration/', include('administrator.urls'),
    url(r'^customer/', include('customer.urls'))

]
