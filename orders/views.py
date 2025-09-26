from rest_framework import viewsets, permissions
from .models import Customer, Inventory, Order, Transaction
from .serializers import (
    CustomerSerializer,
    InventorySerializer,
    OrderSerializer,
    TransactionSerializer,
)


class CustomerViewSet(viewsets.ModelViewSet):
    """CRUD for Customers"""
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]


class InventoryViewSet(viewsets.ModelViewSet):
    """CRUD for Inventory"""
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderViewSet(viewsets.ModelViewSet):
    """CRUD for Orders (scoped to logged-in user’s customers)"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # If user is anonymous (token invalid), return empty queryset
        if not user or not user.is_authenticated:
            return Order.objects.none()

        # Assuming you link Customer → Django User (via customer.user ForeignKey)
        return Order.objects.filter(customer__user=user)


class TransactionViewSet(viewsets.ModelViewSet):
    """CRUD for Transactions"""
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
