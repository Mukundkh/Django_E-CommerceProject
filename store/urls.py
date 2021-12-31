from django.urls import path
from . import views
from .views import *
urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('getReq/', views.product_list),
    path('demo', DemoView.as_view),
]
