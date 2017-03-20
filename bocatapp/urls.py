from django.conf.urls import include, url
from django.contrib import admin
from .decorators import anonymous_required, login_required
from django.contrib.auth.views import login, logout
from bocatapp.views import home, UserRegister, UserAccount

urlpatterns = [
    # Examples:
    url(r'^$', home.home, name='home'),

    # User ==================================================================
    url(r'^user/myAccount/$', login_required(UserAccount.UserAccountView.as_view()), name='myAccount'),
    url(r'^user/edit$', login_required(UserAccount.UserEdit.as_view()), name='editPassword'),
    url(r'^user/myAccount/edit$', login_required(UserAccount.UserEdit.as_view()), name='editAccount'),

    # session ==================================================================

    url(r'^login/$', anonymous_required(login,
                                        message='You`ve already sign in!'), {'template_name': 'auth/login.html'}),
    url(r'^logout/$', logout, {'next_page': '/'}),

    # Admin ==================================================================
    url(r'^administration/', include('administration.urls')),
    url(r'^admin/', admin.site.urls),

    # Seller ==================================================================
    url(r'^seller/register/$', anonymous_required(UserRegister.RegistrationSellerView.as_view(),
                                                  message='You`ve already sign in!'), name='user_register'),
    url(r'^seller/', include('seller.urls')),

    # Customer ==================================================================
    url(r'^customer/', include('customer.urls')),
    url(r'^customer/register/$', anonymous_required(UserRegister.RegistrationCustomerView.as_view(),
                                                    message='You`ve already sign in!'), name='user_register'),
]
