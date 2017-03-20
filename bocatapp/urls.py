from django.conf.urls import include, url
from django.contrib import admin
from .decorators import anonymous_required
from django.contrib.auth.views import login, logout
from bocatapp.views import RegistrationSellerView, RegistrationCustomerView

urlpatterns = [
    # Examples:
    url(r'^$', 'bocatapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^login/$', anonymous_required(login,
                                        message='You`ve already sign in!'),
        {'template_name': 'auth/login.html'}),
    url(r'^logout/$', logout, {'next_page': '/'}),
    # url(r'^signup/$', views.signup),
    url(r'^admin/', admin.site.urls),
    url(r'^seller/register/$', anonymous_required(RegistrationSellerView.as_view(),
                                                  message='You`ve already sign in!'), name='user_register'),
    url(r'^seller/', include('seller.urls')),
    url(r'^administration/', include('administration.urls')),
    url(r'^customer/register/$', anonymous_required(RegistrationCustomerView.as_view(),
                                                    message='You`ve already sign in!'), name='user_register'),
    url(r'^customer/', include('customer.urls')),
]
