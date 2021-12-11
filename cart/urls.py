from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static

# app_name = 'cart'

urlpatterns = [
    path('', views.cart, name="cart"),
    path('carti/<str:pk>', views.carti, name="carti"),
    path('removeItem/<str:pk>', views.removeItem, name="remove-item")
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
