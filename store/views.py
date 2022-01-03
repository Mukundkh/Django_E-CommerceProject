from django.shortcuts import render
from .models import *
#adding required and importing classes
#
from rest_framework.permissions import BasePermission

from .serializers import ProductItemSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# Create your views here.
def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        
    context = {'items' : items}
    return render(request, 'store/cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)

# #creating api's of Product item
# @api_view(['GET','POST'])
# def product_list(request):
#     if request.method == 'GET':
#         products = Product.objects.all()
#         serializer = ProductItemSerializer(products, many=True)
#         return Response(serializer.data)
    
#     elif request.method == 'POST':
#         serializer = ProductItemSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET','PUT','DELETE','PATCH'])
# def product_by_key(request, pk):
#     try:
#         products = Product.objects.get(pk=pk)
    
#     except Product.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == 'GET':
#         serializer = ProductItemSerializer(products)
#         return Response(serializer.data)
    
#     elif request.method == 'PUT':
#         serializer = ProductItemSerializer(products, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer._data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     elif request.method == 'PATCH':
#         serializer = ProductItemSerializer(products, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
#     elif request.method == 'DELETE':
#         products.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# ##
