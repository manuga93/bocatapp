from django.conf.urls import include, url
from django.contrib import admin
from .decorators import anonymous_required, login_required
from django.contrib.auth.views import login, logout,password_reset,password_reset_done, password_reset_confirm, password_reset_complete
from bocatapp.views import home, UserRegister, UserAccount, ShoppingCart
from seller import views
from django.views.generic import TemplateView
from views.TranlateView import change_language
from django.utils.translation import ugettext_lazy as _

urlpatterns = [
    # Examples:
    url(r'^$', home.home, name='home'),#../templates/passwordreset/
    url(r'^reset/password_reset', password_reset,
        {'template_name':'../templates/passwordreset/password_reset_form.html',
        'email_template_name': '../templates/passwordreset/password_reset_email.html'},
        name='password_reset'),
    url(r'^password_reset_done', password_reset_done,
        {'template_name': '../templates/passwordreset/password_reset_done.html'},
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', password_reset_confirm,
        {'template_name': '../templates/passwordreset/password_reset_confirm.html'},
        name='password_reset_confirm'
        ),
    url(r'^reset/done', password_reset_complete, {'template_name': '../templates/passwordreset/password_reset_complete.html'},
        name='password_reset_complete'),
    # User ==================================================================
    url(r'^user/myAccount/$', login_required(UserAccount.UserAccountView.as_view()), name='myAccount'),
    url(r'^user/account/password$', login_required(UserAccount.PasswordEdit.as_view()), name='edit_password'),
    url(r'^user/account/edit$', login_required(UserAccount.UserEdit.as_view()), name='edit_profile'),

    # session ==================================================================

    url(r'^login/$', anonymous_required(login,
                                        message=_('You`ve already sign in!')), {'template_name': 'auth/login.html'}, name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}),

    # Admin ==================================================================
    url(r'^administration/', include('administration.urls')),
    url(r'^admin/', admin.site.urls),

    # Seller ==================================================================
    url(r'^seller/register/$', anonymous_required(UserRegister.RegistrationSellerView.as_view(),
                                                  message=_('You`ve already sign in!')), name='seller_register'),
    url(r'^seller/', include('seller.urls')),
    url(r'^pack/all/$', views.packs_list, name="packs_all"),
    url(r'^pack/local/(?P<pk>[0-9]+)/$', views.local_packs, name="packs_local"),


    # Customer ==================================================================
    url(r'^customer/', include('customer.urls')),
    url(r'^customer/register/$', anonymous_required(UserRegister.RegistrationCustomerView.as_view(),
                                                    message=_('You`ve already sign in!')), name='customer_register'),

    # ShoppingCart ==============================================================
    url(r'^shoppingcart/list/(?P<pk>[0-9]+)/$', ShoppingCart.list_shopping_cart, name='list_shoppingcart'),
    url(r'^shoppingCart/create/', ShoppingCart.create_shopping_cart, name='create_shoppingcart'),
    url(r'^shoppingCart/update_cookie/', ShoppingCart.update_cookie, name='update_cookie'),
    url(r'^shoppingCart/add/', ShoppingCart.add_product, name='add_product_cart'),
    url(r'^ShoppingCart/update/', ShoppingCart.update_product, name='update_product_cart'),
    url(r'^ShoppingCart/delete/', ShoppingCart.delete_product, name='delete_product_cart'),
    url(r'^shoppingCart/update_badge/', ShoppingCart.update_badge, name='update_badge'),
    url(r'^shoppingCart/update_total/', ShoppingCart.update_total, name='update_total'),

    # OTHERS ==================================================================
    url(r'^faq/', TemplateView.as_view(template_name="faq.html"), name='faq'),
    url(r'^terms/', TemplateView.as_view(template_name="terms.html"), name='terms'),
    url(r'^cookies/', TemplateView.as_view(template_name="cookies.html"), name='cookies'),

    # i18n
    url(r'i18n/change_language', change_language, name='change_language'),

]
