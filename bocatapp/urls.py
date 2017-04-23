from django.conf.urls import include, url
from django.contrib import admin
from .decorators import anonymous_required, login_required
from django.contrib.auth.views import login, logout
from bocatapp.views import home, UserRegister, UserAccount, ShoppingCart
from seller import views
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
                                                  message='You`ve already sign in!'), name='seller_register'),
    url(r'^seller/', include('seller.urls')),
    url(r'^pack/all/$', views.packs_list, name="packs_all"),


    # Customer ==================================================================
    url(r'^customer/', include('customer.urls')),
    url(r'^customer/register/$', anonymous_required(UserRegister.RegistrationCustomerView.as_view(),
                                                    message='You`ve already sign in!'), name='customer_register'),

    # ShoppingCart ==============================================================
    url(r'^shoppingcart/list/(?P<pk>[0-9]+)/$', ShoppingCart.list_shopping_cart, name='list_shoppingcart'),
    url(r'^shoppingCart/create/', ShoppingCart.create_shopping_cart, name='create_shoppingcart'),
    url(r'^shoppingCart/update_cookie/', ShoppingCart.update_cookie, name='update_cookie'),
    url(r'^shoppingCart/add/', ShoppingCart.add_product, name='add_product_cart'),
    url(r'^ShoppingCart/update/', ShoppingCart.update_product, name='update_product_cart'),
    url(r'^ShoppingCart/delete/', ShoppingCart.delete_product, name='delete_product_cart'),
    url(r'^shoppingCart/update_badge/', ShoppingCart.update_badge, name='update_badge'),
    url(r'^shoppingCart/update_total/', ShoppingCart.update_total, name='update_total'),
]
