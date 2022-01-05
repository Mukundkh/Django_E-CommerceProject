from django.urls import path

from cart.views import CartAPIView, CheckProductInCart

urlpatterns = [
    path('', CartAPIView.as_view()),
    path('<product_id>/', CheckProductInCart.as_view()),
]
