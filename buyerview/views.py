from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from base.models import Profile
from sellerView.models import Order
# Create your views here.


@login_required(login_url='login')
def buyer(request):
    user = request.user
    pr_obj = Profile.objects.filter(user=user).first()
    orders = Order.objects.filter(bought_by=pr_obj)
    return render(request, 'buyerview/buyer_view.html', {'orders': orders})
