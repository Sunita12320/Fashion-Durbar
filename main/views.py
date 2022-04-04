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
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import *
import uuid
from django.core.mail import send_mail
from .helpers import send_forget_password_mail
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

def productlistAjax(request):
    products = Product.objects.filter(status=0).values_list('name', flat=True)
    productList = list(products)

    return JsonResponse(productList, safe=False)

def searchproduct(request):
    if request.method == 'POST':
        searchedterm = request.POST.get('productsearch')
        if searchedterm == "":
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            product = Product.objects.filter(name__contains=searchedterm).first()

            if product:
                return redirect('collection/'+product.category.slug+'/'+product.slug)
            else:
                messages.info(request,"No product matched your search")
                return redirect(request.META.get('HTTP_REFERER')) 


    return redirect(request.META.get('HTTP_REFERER'))   

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


def handleSignup(request):

    if request.method == "POST":
        #Get the parameters
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        pass1  = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        #check for errorneous inputs
      
        if len(username)>10:
            messages.error(request, "SignUp Unsuccessful 🙁 Username should be under 10 characters !!")
            return redirect('/register')

        if not username.isalnum():
            messages.error(request, "SignUp Unsuccessful 🙁 Username should only have letters and numbers !!")
            return redirect('/register')

        if User.objects.filter(username=username).first():
            messages.error(request, "This username is already registered!! Sorry type unique username")
            return redirect('/register')

        if User.objects.filter(email = email).first():
            messages.success(request, "Email is taken.")
            return redirect('/register')
            
        if len(pass1)<8:
            messages.error(request, "The password should be of atleast of 8 characters")
            return redirect('/register')

        if re.search('[0-9]', pass1) is None:
            messages.error(request, "The password should have a number in it")
            return redirect('/register')

        # if re.search('[A-Z]',pass1) is None:
        #     messages.error(request, "The password should have a capital letter in it")
        #     return redirect('/register')

        # if re.search('[@, $, #]',pass1) is None:
        #     messages.error(request, "The password should have symbols like [@, $, #]")
        #     return redirect('/register')

        if pass1 != pass2:
            messages.warning(request, "SignUp Unsuccessful 🙁 Passwords do not match !!")
            return redirect('/register')
                    # return render(request, 'codes/SignUp.html')

        #create users
        myuser = User.objects.create_user(username, email,pass1)
        myuser.set_password(pass1)
        myuser.phone = phone
        myuser.save()
        auth_token = str(uuid.uuid4())
        profile_obj = Profile.objects.create(user=myuser, auth_token=auth_token)
        profile_obj.save()
        send_mail_after_registration(email, auth_token)
        return redirect('/token')
    else:
        return redirect('/signup')
        

def handleLogin(request):
    if request.method == "POST":
        #Get the parameters
        loginname=request.POST.get('loginname')
        loginpass=request.POST.get('loginpass')

        user_obj = User.objects.filter(username = loginname).first()

        if user_obj is None:
            messages.success(request, 'User not found')
            return redirect('/signin')
        
        profile_obj = Profile.objects.filter(user = user_obj).first()

        if not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified yet please check your mail!')
            return redirect('/login') 
        
        user = authenticate(username=loginname, 
        password=loginpass)
       
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

   
def success(request):
    return render(request, 'sunita/success.html')

def token_send(request):
    return render(request, 'sunita/token_send.html')

def verify(request, auth_token):
    profile_obj = Profile.objects.filter(auth_token = auth_token).first()
    if profile_obj:
        if profile_obj.is_verified:
            messages.success(request, "Your account has already verified!")
            return redirect('/signin')

        profile_obj.is_verified = True
        profile_obj.save()
        messages.success(request, "Your account has been verified..")
        return redirect('/signin')
    else: 
        return redirect('/error')

def error_page(request):
    return render(request, 'sunita/error.html')


def send_mail_after_registration(email, token):
    subject ='Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)

def ChangePassword(request , token):
    context = {}
    
    profile_obj = Profile.objects.filter(forget_password_token = token).first()
    context = {'user_id' : profile_obj.user.id}
        
    if request.method == 'POST':
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        user_id = request.POST.get('user_id')
            
        if user_id is  None:
            messages.error(request, 'No user id found.')
            return redirect(f'/change-password/{token}/')
                      
        if  pass1 != pass2:
            messages.success(request, 'both should  be equal.')
            return redirect(f'/change-password/{token}/')
                         
            
        user_obj = User.objects.get(id = user_id)
        user_obj.set_password(pass1)
        user_obj.save()
        return redirect('/login')
            
    return render(request , 'sunita/change-password.html' , context)

def ForgetPassword(request):
     if request.method =='POST':
        username = request.POST.get('username')

        if not User.objects.filter(username=username).first():
            messages.success(request,'Not user found with this username.')
            return redirect('/forget-password')
        
        user_obj = User.objects.get(username = username)
        token = str(uuid.uuid4())
        profile_obj= Profile.objects.get(user = user_obj)
        profile_obj.forget_password_token = token
        profile_obj.save()
        send_forget_password_mail(user_obj.email, token)
        messages.success(request,'An email is sent to your account, please check your mail...')
        return redirect('/forget-password')

     return render(request,'sunita/forget-password.html')
 