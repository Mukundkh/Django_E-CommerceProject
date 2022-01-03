from store.models import Product, Customer, Order, OrderItem, ShippingAddress
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from store.api.serializers import ProductItemSerializer
from store.api.permissions import AdminOrReadOnly

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
#@permission_classes([AdminOrReadOnly])
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductItemSerializer(products, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProductItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE','PATCH'])
def product_by_key(request, pk):
    try:
        products = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ProductItemSerializer(products)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ProductItemSerializer(products, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PATCH':
        serializer = ProductItemSerializer(products, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        products.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)