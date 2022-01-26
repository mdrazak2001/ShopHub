import plotly.express as px
import plotly.offline as opy
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
import numpy as np
import pandas as pd
from sellerView.models import Order
from sellerView.views import seller
from .pdf import *
# Create your views here.


@login_required(login_url='login')
def Orders(request):
    if not request.user.is_superuser:
        return redirect('home')
    orders = Order.objects.all()
    context = {}
    context['orders'] = orders
    return render(request, 'adminview/orders.html', context)


@login_required(login_url='login')
def generatePdf(request):
    if not request.user.is_superuser:
        return redirect('home')
    orders = Order.objects.all()
    context = {}
    context['orders'] = orders
    pdf = render_to_pdf('adminview/order_pdf.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Orders_Invoice.pdf"
        content = "inline; filename='%s'" % (filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")


@login_required(login_url='login')
def graph(request):
    context = {}
    orders = orders = Order.objects.all()
    products = []
    dates = []
    prices = []
    np_array = []
    for order in orders:
        time = order.time
        # time = time.date()
        product = order.product.product_name
        price = int(order.product.price_in_rupees)
        seller = order.sold_by.user.username
        buyer = order.bought_by.user.username

        products.append(product)
        dates.append(time)
        prices.append(price)
        np_array.append([product, price, time, seller, buyer])
    array = np.array(np_array)
    column_values = ['Product', 'Price', 'Time', 'Seller', 'Buyer']
    df = pd.DataFrame(data=array, columns=column_values)
    print(df)

    fig = px.line(
        data_frame=df,
        x='Time',
        y='Price',
        custom_data=['Product', 'Price', 'Time', 'Seller', 'Buyer'],
        markers=True,

    )
    fig.update_layout(
        hovermode="x",
    )
    fig.update_traces(
        hovertemplate="<br>".join([
            "Product: %{customdata[0]}",
            "Price: %{y}",
            "Seller: %{customdata[3]}",
            "Buyer: %{customdata[4]}",
        ])
    )

    div = opy.plot(fig, auto_open=False, output_type='div')
    context['fig'] = div

    return render(request, 'adminview/graph.html', context)
