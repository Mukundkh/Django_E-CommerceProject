from django.urls import path
from store.api import views

urlpatterns = [
    path('getAllProducts/', views.ProductList.as_view()),
    path('getAllProducts/<int:pk>/', views.ProductDetail.as_view()),
]
