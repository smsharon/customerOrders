from rest_framework import viewsets, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework.response import Response
from .models import Customer, Inventory, Order, Transaction
from .serializers import (
    CustomerSerializer,
    InventorySerializer,
    OrderSerializer,
    TransactionSerializer,
)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        data = request.data

        # check duplicate username
        if User.objects.filter(username=data['code']).exists():
            return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # create auth user
        user = User.objects.create_user(
            username=data['code'],
            password=data['password'],
            email=data.get('email', '')
        )

        # create customer profile linked to user
        customer = Customer.objects.create(
            user=user,
            name=data['name'],
            code=data['code'],
            phone_number=data['phone_number']
        )

        return Response(CustomerSerializer(customer).data, status=status.HTTP_201_CREATED)

class InventoryViewSet(viewsets.ModelViewSet):
    """CRUD for Inventory"""
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return orders for the authenticated customer
        try:
            customer = Customer.objects.get(user=self.request.user)
            return Order.objects.filter(customer=customer)
        except Customer.DoesNotExist:
            return Order.objects.none()

    def perform_create(self, serializer):
        # Link order to authenticated customer
        customer = Customer.objects.get(user=self.request.user)
        order = serializer.save(customer=customer)
        # Send SMS
        from .signals import send_sms
        message = f"Dear {customer.name}, your order #{order.id} has been placed."
        send_sms(customer.phone_number, message)


class TransactionViewSet(viewsets.ModelViewSet):
    """CRUD for Transactions"""
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]