
from . import views
from django.urls import path , include



urlpatterns =[
    path('',views.index, name='home'),
    path('collection',views.collection, name='collection'),
    path('collection/<str:slug>', views.collectionview, name="collectionview"),
    path('collection/<str:cat_slug>/<str:prod_slug>', views.productview, name="productview"),
    path('about',views.about, name='about'),
    path('cart',views.viewcart, name='cart'),
    path('update-cart',views.updatecart, name='updatecart'),
    path('delete-cart-item',views.deletecartitem, name='deletecartitem'),
    path('contact',views.contact, name='contact'),
    path('register',views.register, name='register'),
    path('signin',views.signin, name='signin'),
    path('signup',views.handleSignup, name='handleSignup'),
    path('login',views.handleLogin, name='handleLogin'),
    path('logout',views.handleLogout, name='handleLogout'),
    path('add-to-cart',views.addtocart, name='addtocart'),
]