from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
import pytz

from sellerView.models import Order
from .models import *
from django.contrib.auth.models import User
from base.models import *
import time
from datetime import datetime
from django.utils import timezone
# Create your views here.


def get_localtime(utctime):
    utc = utctime.replace(tzinfo=pytz.UTC)
    localtz = utc.astimezone(timezone.get_current_timezone())
    return localtz


@login_required(login_url='login')
def cart(request):
    user = request.user
    # print(user.first_name, user.last_name)
    cart = {}
    try:
        pr_obj = Profile.objects.filter(user=user).first()
        cart = Cart.objects.filter(user=pr_obj).first()
    except Exception as e:
        print(e)

    if request.method == 'POST':
        pr_obj = Profile.objects.filter(user=user).first()
        cart = Cart.objects.filter(user=pr_obj).first()
        cart_items = CartItem.objects.filter(cart=cart)
        for ci in cart_items:
            # print(ci.product.product_name)
            email = ci.product.created_by.user.email
            product = ci.product.product_name
            price = ci.product.price_in_rupees
            phone = cart.user.phone
            buyer = user.first_name, user.last_name
            print(buyer)
            ci.product.is_sold = True
            ci.product.save()
            now = get_localtime(datetime.now())
            order = Order.objects.create(sold_by=ci.product.created_by,
                                         bought_by=pr_obj, product=ci.product, time=now, price=price)
            order.save()
            ci.delete()
            send_mail_to_vendor(email, product, buyer, phone, price)
        cart.total_price = 0
        cart.save()

    return render(request, 'cart/cart.html', {'user': user, 'cart': cart})


def send_mail_to_vendor(email, product, buyer, phone, price):
    subject = f'Product {product} Sold'
    message = f'Your product {product} has been bought !!! by {buyer}, phone number : {phone}'
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email])


def carti(request, pk):
    return redirect(f'/product/{pk}')


def removeItem(request, pk):
    cart_item = CartItem.objects.get(id=pk)
    price_of_product = Product.objects.get(id=cart_item.product.id)
    if cart_item is not None:
        cart = cart_item.cart
        cart.total_price -= price_of_product.price_in_rupees
        cart.save()
        cart_item.delete()
    return redirect('cart')
