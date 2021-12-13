from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from base.models import Profile
from sellerView.models import Order
# Create your views here.


@login_required(login_url='login')
def buyer(request):
    user = request.user
    pr_obj = Profile.objects.filter(user=user).first()
    orders = Order.objects.filter(bought_by=pr_obj)
    return render(request, 'buyerview/buyer_view.html', {'orders': orders})


@login_required(login_url='login')
def VerfiyOrderCompletion(request, pk):
    order = Order.objects.get(id=pk)
    user = request.user
    buyer = order.bought_by
    pr_ob = Profile.objects.filter(user=user).first()
    if(pr_ob != buyer):
        return redirect('home')

    if request.method == 'POST':
        order.completed = True
        order.save()

    return render(request, 'buyerview/verify.html', {'order': order})
