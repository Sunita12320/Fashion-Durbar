from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import re
from django.conf import urls
from matplotlib.style import context
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import *
def index(request):
    # products = FeatureProduct.objects.all()
    # print(products)
    # context = {'products': products}
    trending_products = Product.objects.filter(trending=1)
    context ={'trending_products':trending_products}
    return render(request, 'sunita/home.html',context=context)

def collection(request):
    category = Category.objects.filter(status=0)
    context = {'category':category}
    return render(request, 'sunita/collection.html', context)

def collectionview(request, slug):
    if(Category.objects.filter(slug=slug, status=0)):
        product = Product.objects.filter(category__slug=slug)
        category = Category.objects.filter(slug=slug).first()
        context = {'product':product, 'category':category}
        
        return render(request, "sunita/product/product.html",context)
    else:
        messages.warning(request, "No such category was found")
        return redirect('/collection')

def productview(request, cat_slug, prod_slug):
    if(Category.objects.filter(slug=cat_slug, status =0)):
        if(Product.objects.filter(slug=prod_slug, status =0)):
            product = Product.objects.filter(slug=prod_slug, status =0).first
            context = {'product':product}
    
        else:
            messages.error(request, "No such category found")
            return redirect('/collection')
        
    else:
        messages.error(request, "No such category found")
        return redirect('/collection')
    return render(request, "sunita/product/productview.html",context)

   
def addtocart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if(product_check):
                if(Cart.objects.filter(user=request.user.id, product_id =prod_id)):
                    return JsonResponse({'status':"Product Already in Cart"})
                     
                else:
                    prod_qty = int(request.POST.get('product_qty'))
                    if product_check.quantity >= prod_qty:
                        Cart.objects.create(user=request.user,product_id= prod_id, product_qty=prod_qty)
                        return JsonResponse({'status':"Product added successfully 🙂"})
                        
                    else:
                        return JsonResponse({'status':"Only "+str(product_check.quantity)+" quantity available"})

                        

            
            else:
                return JsonResponse({'status':"No such product found"})
        
        else:
            return JsonResponse({'status':"Please proceed to login!!"})
    return redirect('/')

def about(request):
    return render(request, 'sunita/about.html')

def viewcart(request):
    cart = Cart.objects.filter(user=request.user)
    context ={'cart':cart}
    return render(request, 'sunita/cart.html',context)

def updatecart(request):
    if request.method=="POST":
        prod_id = int(request.POST.get('product_id'))
        if(Cart.objects.filter(user=request.user, product_id=prod_id)):
            prod_qty = int(request.POST.get('product_qty'))
            cart = Cart.objects.get(product_id=prod_id, user= request.user)
            cart.product_qty = prod_qty
            cart.save()
            return JsonResponse({'status':"Updated Successfully"})
    return redirect('/collection')       
   
def deletecartitem(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if(Cart.objects.filter(user=request.user, product_id=prod_id)):
            cartitem= Cart.objects.get(product_id=prod_id, user = request.user)
            cartitem.delete()
        return JsonResponse({'status': "Deleted Successfully"}) 
    return redirect('/collection') 



def contact(request):
    return render(request, 'sunita/contact.html')

def register(request):
    return render(request, 'sunita/register.html')

def signin(request):
    return render(request, 'sunita/signin.html')

# def handleSignup(request):
#     if request.method == 'POST':
        
#         name = request.POST['name']
#         email = request.POST['email']
#         phone = request.POST['phone']
#         pass1  = request.POST['pass1']
#         pass2 = request.POST['pass2']

       
#         myuser = User.objects.create_user(name, email, pass1)
#         myuser.phone = phone 
#         myuser.save()
#         messages.success(request, "Your acount has been successfully created")
#         return redirect('home')


#     else:
#         return HttpResponse('404 - Not Found')


def handleSignup(request):
    if request.method == "POST":
        #Get the parameters
        name=request.POST['name']
        email=request.POST['email']
        phone = request.POST['phone']
        pass1  = request.POST['pass1']
        pass2 = request.POST['pass2']

        #check for errorneous inputs
       
        if len(name)>10:
            messages.error(request, "SignUp Unsuccessful 🙁 Username should be under 10 characters !!")
            return redirect('/register')

        if not name.isalnum():
            messages.error(request, "SignUp Unsuccessful 🙁 Username should only have letters and numbers !!")
            return redirect('/register')

        if User.objects.filter(username=name).first():
            messages.error(request, "This username is already registered!! Sorry type unique username")
            return redirect('/register')

        if len(pass1)<8:
            messages.error(request, "The password should be of atleast of 8 characters")
            return redirect('/register')

        if re.search('[0-9]', pass1) is None:
            messages.error(request, "The password should have a number in it")
            return redirect('/register')

        if re.search('[A-Z]',pass1) is None:
            messages.error(request, "The password should have a capital letter in it")
            return redirect('/register')

        if re.search('[@, $, #]',pass1) is None:
            messages.error(request, "The password should have symbols like [@, $, #]")
            return redirect('/register')

        if pass1 != pass2:
            messages.warning(request, "SignUp Unsuccessful 🙁 Passwords do not match !!")
            return redirect('/register')
            # return render(request, 'codes/SignUp.html')

        #create users
        myuser = User.objects.create_user(name, email, pass1)
        myuser.phone = phone
        myuser.save()
        messages.success(request, "SignUp Successful 🙂")
        return redirect('/')
        

    else:
        # return HttpResponse('404 - Not Found')
        return render(request, 'sunita/register.html')


def handleLogin(request):
    if request.method == "POST":
        #Get the parameters
        loginname=request.POST['loginname']
        loginpass=request.POST['loginpass']
        
        user = authenticate(username=loginname, 
        password=loginpass)
        try:
           remember = request.POST['remember-me']
           if remember:
                    settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
        except:
            settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True


        if user is not None:
            login(request, user)
            messages.success(request, "Successfuly Logged In")
            return redirect('/')
            
        else:
            messages.warning(request, "Invalid Credentials, Please try again!!")
            return redirect('/signin')

    return render(request, 'sunita/signin.html')

def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out!!!")
    return redirect('/')

    return HttpResponse('handleLogout')

   
    
