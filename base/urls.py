from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    # path('buyer/login/', views.buyerLogin, name="buyer-login"),
    # path('buyer/register/', views.buyerRegister, name="buyer-register"),
]
