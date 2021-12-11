from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth.models import User
from base.models import *
# Create your views here.


def cart(request):
    user = request.user
    cart = {}
    try:
        pr_obj = Profile.objects.filter(user=user).first()
        cart = Cart.objects.filter(user=pr_obj).first()
    except Exception as e:
        print(e)
    return render(request, 'cart/cart.html', {'user': user, 'cart': cart})


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
