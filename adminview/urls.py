from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static


urlpatterns = [
    path('orders', views.Orders, name="orders"),
    path('orders/generatepdf', views.generatePdf, name="generate-pdf-order"),
    path('graph/', views.graph, name="graph_"),
]
