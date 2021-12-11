from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from base.models import *
from sellerView.models import Order
# Create your views here.


@login_required(login_url='login')
def seller(request):
    # print(request.path)
    path = request.path
    return render(request, 'sellerView/seller_home.html')


def viewProducts(request):
    user = request.user
    pr_obj = Profile.objects.filter(user=user).first()
    products = Product.objects.filter(created_by=pr_obj)

    return render(request, 'sellerView/products.html', {'products': products})


def soldProducts(request):
    user = request.user
    pr_obj = Profile.objects.filter(user=user).first()
    orders = Order.objects.filter(sold_by=pr_obj)
    return render(request, 'sellerView/sold_products.html', {'orders': orders})
