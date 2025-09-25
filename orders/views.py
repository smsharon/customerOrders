from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Customer, Inventory, Order, Transaction
from .serializers import CustomerSerializer, InventorySerializer, OrderSerializer, TransactionSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()  # 👈 add this line
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(customer__user=user)

    
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer      
    
