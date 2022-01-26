import numpy as np
import pandas as pd
import plotly.graph_objects as go
import datetime as dt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import context
from base.models import *
from sellerView.forms import DateTimeInput
from sellerView.models import Order
from django.core.mail import send_mail
from django.conf import settings
import time
from background_task import background
import plotly.express as px
import plotly.offline as opy


@login_required(login_url='login')
def seller(request):
    # print(request.path)
    path = request.path
    return render(request, 'sellerView/seller_home.html')


@login_required(login_url='login')
def viewProducts(request):
    user = request.user
    pr_obj = Profile.objects.filter(user=user).first()
    products = Product.objects.filter(created_by=pr_obj)

    return render(request, 'sellerView/products.html', {'products': products})


@login_required(login_url='login')
def soldProducts(request):
    user = request.user
    pr_obj = Profile.objects.filter(user=user).first()
    orders = Order.objects.filter(sold_by=pr_obj)
    return render(request, 'sellerView/sold_products.html', {'orders': orders})


@login_required(login_url='login')
def graph(request):
    context = {}
    user = request.user
    pr_obj = Profile.objects.filter(user=user).first()
    orders = Order.objects.filter(sold_by=pr_obj)
    print(orders)
    products = []
    dates = []
    prices = []
    np_array = []
    for order in orders:
        time = order.time
        # time = time.date()
        product = order.product.product_name
        price = int(order.product.price_in_rupees)
        products.append(product)
        dates.append(time)
        prices.append(price)
        np_array.append([product, price, time])

    array = np.array(np_array)
    column_values = ['Product', 'Price', 'Time']
    df = pd.DataFrame(data=array, columns=column_values)
    # print(df)

    fig = px.line(
        data_frame=df,
        x='Time',
        y='Price',
        custom_data=['Product', 'Price', 'Time'],
        markers=True
    )
    fig.update_layout(
        hovermode="x",
    )

    fig.update_traces(
        hovertemplate="<br>".join([
            "Product: %{customdata[0]}",
            "Price: %{y}",
        ])
    )

    div = opy.plot(fig, auto_open=False, output_type='div')
    context['fig'] = div

    return render(request, 'sellerView/graph.html', context)


@login_required(login_url='login')
def Action(request, pk):
    form = DateTimeInput()
    if request.method == 'POST':
        delivery_time = request.POST['delivery_time']
        delivery_time.replace('T', ' ', 1)
        # str = string(delivery_time)
        # print(delivery_time)
        str_delivery_time = ''
        for c in delivery_time:
            if c != 'T':
                str_delivery_time += c
            else:
                str_delivery_time += ' '
        # print(str_del_time)
        str_delivery_time += ':0'
        delivery_time_obj = dt.datetime.strptime(
            str_delivery_time, '%Y-%m-%d %H:%M:%S')
        now = dt.datetime.now()
        diff = delivery_time_obj - now
        seconds = diff.total_seconds()
        order_ob = Order.objects.get(id=pk)
        seconds = int(seconds)
        notify_buyer(order_ob.id, schedule=seconds)

    return render(request, 'sellerView/action.html', {'form': form})


def send_mail_to_buyer(email, product, seller, phone, price, order_id):
    subject = f'Product {product} Reached You!!'
    message = f'Your product {product}  should reach you by now !!! by seller {seller}, phone number : {phone}, Please Pay {price} /- \n Please Click on this Link If Youve Recieved The Product http://127.0.0.1:8000/buyer/verifyorder/{order_id} \n Thanks For Buying !!'
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email])


@background(schedule=60)
def notify_buyer(order_id):
    order_ob = Order.objects.get(id=order_id)
    seller = Profile.objects.filter(id=order_ob.sold_by.id).first()
    buyer = Profile.objects.filter(id=order_ob.bought_by.id).first()
    product = order_ob.product.product_name
    send_mail_to_buyer(buyer.user.email, product, seller.user.first_name,
                       seller.phone, order_ob.product.price_in_rupees, order_id)
