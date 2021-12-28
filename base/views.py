from django.db.models import Q
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages

from cart.models import *
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
import os
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from django.http import HttpResponseRedirect
import time
from .mail import *
from datetime import datetime
from django.utils import timezone
import pytz
from .singular import *

# Create your views here.


def get_localtime(utctime):
    utc = utctime.replace(tzinfo=pytz.UTC)
    localtz = utc.astimezone(timezone.get_current_timezone())
    return localtz


def home(request):
    # print("1")
    context = {}
    q = request.GET.get('q')
    products = Product.objects.all()
    if q is not None:
        q1 = convertToSingular(q)
        products = Product.objects.filter(
            Q(product_name__icontains=q) |
            Q(product_name__icontains=q1)
        )

    context['products'] = products
    return render(request, 'base/home.html', context)


def userLogout(request):
    logout(request)
    return redirect('home')


def userLogin(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_ob = User.objects.filter(username=username).first()
        if user_ob is None:
            messages.add_message(request, messages.INFO, 'User not found')
            return redirect('login')
        profile_ob = Profile.objects.filter(user=user_ob).first()
        if profile_ob is None:
            user = authenticate(username=username, password=password)
            if user is None:
                messages.add_message(request, messages.INFO,
                                     'Wrong creds')
                return redirect('login')
            login(request, user)
            return redirect('home')
        elif profile_ob.is_verified == False:
            messages.add_message(request, messages.INFO,
                                 'Your profile isnt verified check your mail')
            return redirect('login')
        else:
            user = authenticate(username=username, password=password)
            if user is None:
                messages.add_message(request, messages.INFO,
                                     'Wrong creds')
                return redirect('login')
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('home')
    page = 'login'
    return render(request, 'base/login_register.html', {'page': page})


def userRegister(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        f_name = request.POST['fname']
        l_name = request.POST['lname']
        try:
            if User.objects.filter(email=email).first() is not None:
                messages.add_message(
                    request, messages.INFO, 'email name taken')
                render(request, 'base/login_register.html')

            elif User.objects.filter(username=username).first() is not None:
                messages.add_message(request, messages.INFO, 'User name taken')
                render(request, 'base/login_register.html')

            else:
                user_ob = User.objects.create(
                    username=username, email=email,
                    first_name=f_name, last_name=l_name)
                user_ob.set_password(password)
                user_ob.save()
                auth_token = str(uuid.uuid4())
            now = get_localtime(datetime.now())
            profile_ob = Profile.objects.create(
                user=user_ob, auth_token=auth_token, created_at=now, phone=phone)
            profile_ob.save()
            cart = Cart.objects.create(user=profile_ob)
            cart.save()
            send_mail_after_registration(email, auth_token)
            return redirect('token_send')

        except Exception as e:
            print(e)
    page = 'register'
    return render(request, 'base/login_register.html', {'page': page})


def token_send(request):
    return render(request, 'base/token.html')


def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if(profile_obj.is_verified):
                messages.add_message(
                    request, messages.INFO, 'Your Account is already verified now you can login!!')
                return redirect('login')

            profile_obj.is_verified = True
            profile_obj.save()
            messages.add_message(
                request, messages.INFO, 'Your Account is verified now you can login!!')
            return redirect('login')
        else:
            messages.add_message(
                request, messages.INFO, 'error occured')
    except Exception as e:
        print(e)


@login_required(login_url='login')
def addProduct(request):
    form = ProductForm()
    if request.method == 'POST':
        price = request.POST.get('price_in_rupees')
        product_name = request.POST.get('product_name')
        descripton = request.POST.get('descripton')
        Images = request.FILES.getlist('images')
        # print(Images)
        user = request.user
        id = str(uuid.uuid4())
        now = get_localtime(datetime.now())
        try:
            profile = Profile.objects.filter(user=user).first()
            product_ob = Product.objects.create(created_by=profile, price_in_rupees=price,
                                                product_name=product_name, descripton=descripton, created_at=now)
            # print(user)
            product_ob.save()
            for image in Images:
                pimg = ProductImage.objects.create(
                    images=image, product=product_ob)
                pimg.save()
            time.sleep(1)
            return redirect('home')
        except Exception as e:
            print(e)

    return render(request, 'base/add_product.html', {'form': form})


def forgotPassword(request):
    page = 'forgot'
    if request.user.is_authenticated:
        return redirect('home')
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            if not User.objects.filter(username=username).first():
                messages.add_message(
                    request, messages.INFO, 'no such accout')
                return redirect('forgot-password')

            user_obj = User.objects.filter(username=username).first()
            email = user_obj.email
            profile_obj = Profile.objects.filter(user=user_obj).first()
            auth_token = profile_obj.auth_token
            send_mail_after_forgot(email, auth_token)
            messages.add_message(
                request, messages.INFO, 'Check Mail for reset link')

    except Exception as e:
        print(e)

    return render(request, 'base/login_register.html', {'page': page})


def changePassword(request, auth_token):
    if request.user.is_authenticated:
        return redirect('home')
    token = auth_token
    if request.method == 'POST':
        try:
            profile_obj = Profile.objects.filter(auth_token=token).first()
            if profile_obj is not None:
                p1 = request.POST['p1']
                p2 = request.POST['p2']
                if p1 != p2:
                    messages.add_message(
                        request, messages.INFO, 'Passwords dont match Re enter')
                    return redirect(f'/changepassword/{token}')
                user = profile_obj.user
                uo = User.objects.filter(username=user).first()
                uo.set_password(p1)
                uo.save()
                messages.add_message(
                    request, messages.INFO, 'Password Reset Try Logging in now!')
                time.sleep(1)
                return redirect('login')
            else:
                messages.add_message(
                    request, messages.INFO, 'error occured')
        except Exception as e:
            print(e)

    return render(request, 'base/changepassword.html')


def viewProduct(request, pk):
    context = {}
    product = Product.objects.get(id=pk)
    print(product.product_name)
    context['product'] = product
    return render(request, 'base/product.html', context)


def deleteProduct(request, pk):
    what = 'product'
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'what': what, 'product': product})


@login_required(login_url='login')
def addToCart(request, pk):
    user = request.user
    pr_obj = Profile.objects.filter(user=user).first()
    cart = Cart.objects.filter(user=pr_obj).first()
    product = Product.objects.get(id=pk)
    dup_exists = CartItem.objects.filter(cart=cart, product=product).first()
    if not dup_exists:
        cart_item = CartItem.objects.create(cart=cart, product=product)
        price_of_product = Product.objects.get(id=cart_item.product.id)

        cart = cart_item.cart
        cart.total_price += price_of_product.price_in_rupees
        cart.save()
        cart_item.price = price_of_product.price_in_rupees
        cart_item.save()

    return redirect('cart')
