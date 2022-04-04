import json
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import re
from django.conf import urls
from matplotlib.style import context
from .models import Cart

def index(request):

    rawcart = Cart.objects.filter(user=request.user)
    for item in rawcart:
        if item.product_qty > item.product.quantity:
            Cart.objects.delete(id=item.id)
        
    cartitems = Cart.objects.filter(user = request.user)
    total_price =0 
    for item in cartitems:
        total_price = total_price + item.product.price * item.product_qty

        
    context ={'cartitems':cartitems, 'total_price':total_price}
    
    return render(request, 'sunita/checkout.html', context)

