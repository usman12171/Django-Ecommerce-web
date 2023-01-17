from django.conf import settings
from django.urls import path
from . import views
from  .form import loginform
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name='index'),
    path('emailvalid',views.emailvalids,name='emailvalid'),
    path('cutomerregister',views.customerregister.as_view(),name='customerregister'),
    path('profile',views.updates_profile,name='profile'),
    path('products',views.products,name='products'),
    path('products/<slug:data>',views.products,name='productsdata'),
    path('product_deta/<int:id>',views.product_detail,name='product_deta'),
    path('review',views.review,name='review'),
    path('addcart/',views.add_cart,name='addcart'),
    path('showcart/',views.show_cart,name='showcart'),
    path('removecart/',views.remove_cart,name='removecart'),
    path('pluscart/',views.plus_cart,name='pluscart'),
    path('minuscart/',views.minus_cart,name='minuscart'),
    path('checkout/',views.checkout,name='checkout'),
    path('placeorder/',views.place_order,name='placeorder'),
    path('orders/',views.order,name='orders'),
    path('login',auth_views.LoginView.as_view(template_name='core/login.html',authentication_form=loginform),name='login'),
    path('logout',auth_views.LogoutView.as_view(next_page='index'),name='logout')
    ]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)