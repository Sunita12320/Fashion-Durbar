
from . import views,checkout
from django.urls import path , include



urlpatterns =[
    path('',views.index, name='home'),
    path('collection',views.collection, name='collection'),
    path('collection/<str:slug>', views.collectionview, name="collectionview"),
    path('collection/<str:cat_slug>/<str:prod_slug>', views.productview, name="productview"),
    path('product-list', views.productlistAjax),

    path('searchproduct',views.searchproduct, name='searchproduct'),

    path('about',views.about, name='about'),

    path('cart',views.viewcart, name='cart'),
    path('add-to-cart',views.addtocart, name='addtocart'),
    path('update-cart',views.updatecart, name='updatecart'),
    path('delete-cart-item',views.deletecartitem, name='deletecartitem'),

    path('contact',views.contact, name='contact'),

    path('register',views.register, name='register'),
    path('signin',views.signin, name='signin'),
    path('signup',views.handleSignup, name='handleSignup'),
    path('login',views.handleLogin, name='handleLogin'),
    path('logout',views.handleLogout, name='handleLogout'),
 
    path('token', views.token_send, name='token_send'),
    path('success', views.success, name='success'),
    path('verify/<auth_token>', views.verify, name='verify'),
    path('error', views.error_page, name ='error'),
    path('forget-password/', views.ForgetPassword, name ='forget_password'),
    path('change-password/<token>/' , views.ChangePassword , name="change_password"),

    path('checkout', checkout.index, name='checkout')

]