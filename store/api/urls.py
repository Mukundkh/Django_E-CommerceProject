from django.urls import path
from store.api import views

urlpatterns = [
    path('getAllProducts/', views.product_list),
    path('getAllProducts/<int:pk>/', views.product_by_key),
]
