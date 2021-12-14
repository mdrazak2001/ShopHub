from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from sellerView.models import Order
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
