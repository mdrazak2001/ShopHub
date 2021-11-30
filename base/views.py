from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.
from .models import Profile
import uuid
from django.conf import settings
from django.core.mail import send_mail
import os
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *


def home(request):
    user_products = Product.objects.all()
    # profile specific products
    # try:
    #     if request.user.is_authenticated and not request.user.is_superuser:
    #         user = request.user
    #         for profile in Profile.objects.all():
    #             if profile.user == user:
    #                 user_products = profile.product_set.all()
    # except Exception as e:
    #     print(e)
    return render(request, 'base/home.html', {'user_products': user_products})


def userLogout(request):
    logout(request)
    return redirect('home')


def userLogin(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        # email = request.POST.get('email')
        password = request.POST.get('password')
        user_ob = User.objects.filter(username=username).first()
        if user_ob is None:
            messages.add_message(request, messages.INFO, 'User not found')
            return redirect('login')

        profile_ob = Profile.objects.filter(user=user_ob).first()

        if profile_ob.is_verified == False:
            messages.add_message(request, messages.INFO,
                                 'Your profile isnt verified check your mail')
            return redirect('login')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.add_message(request, messages.INFO,
                                 'Wrong creds')
            return redirect('login')
        login(request, user)
        return redirect('home')
    page = 'login'
    return render(request, 'base/login_register.html', {'page': page})


def userRegister(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            if User.objects.filter(username=username).first():
                messages.add_message(request, messages.INFO, 'User name taken')
                render(request, 'base/login_register.html')

            if User.objects.filter(email=email).first():
                messages.add_message(
                    request, messages.INFO, 'email name taken')
                render(request, 'base/login_register.html')
            user_ob = User.objects.create(username=username, email=email)
            user_ob.set_password(password)
            user_ob.save()
            auth_token = str(uuid.uuid4())

            profile_ob = Profile.objects.create(
                user=user_ob, auth_token=auth_token)
            profile_ob.save()

            send_mail_after_registration(email, auth_token)
            return redirect('token_send')

        except Exception as e:
            print(e)

    return render(request, 'base/login_register.html')


def token_send(request):
    return render(request, 'base/token.html')


def send_mail_after_registration(email, token):
    subject = 'Your account needs to be verified'
    message = f'Hi paste the link to verify you account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email])


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
        photo = request.POST.get('photo')
        user = request.user
        try:
            for profile in Profile.objects.all():
                if profile.user == user:
                    product_ob = Product.objects.create(created_by=profile, price_in_rupees=price,
                                                        product_name=product_name, photo=photo, descripton=descripton)
                    product_ob.save()
        except Exception as e:
            print(e)

    return render(request, 'base/add_product.html', {'form': form})
