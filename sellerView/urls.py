from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static

# app_name = 'cart'

urlpatterns = [
    path('', views.seller, name="seller"),
    path('products/', views.viewProducts, name="products"),
    path('sold/', views.soldProducts, name="sold-products"),
    path('action/<str:pk>', views.Action, name="action"),
    path('graph/', views.graph, name="graph"),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
