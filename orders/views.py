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
    """
    ViewSet for managing Customer records.
    Provides CRUD operations and a custom registration endpoint.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        """
        Custom action to register a new customer.
        Creates a Django auth User and links it with a Customer profile.

        Request body should include:
        - code (used as username)
        - password
        - name
        - phone_number
        - email (optional)

        Returns:
            Response: Serialized Customer data or error message.
        """
        data = request.data

        if User.objects.filter(username=data['code']).exists():
            return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=data['code'],
            password=data['password'],
            email=data.get('email', '')
        )

        customer = Customer.objects.create(
            user=user,
            name=data['name'],
            code=data['code'],
            phone_number=data['phone_number']
        )

        return Response(CustomerSerializer(customer).data, status=status.HTTP_201_CREATED)


class InventoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Inventory items.
    Provides CRUD operations.
    """
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Orders.
    Ensures that only the authenticated customer's orders are visible.
    Links new orders to the logged-in customer and triggers SMS notifications.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Restrict the queryset to orders belonging to the authenticated customer.
        """
        try:
            customer = Customer.objects.get(user=self.request.user)
            return Order.objects.filter(customer=customer)
        except Customer.DoesNotExist:
            return Order.objects.none()

    def perform_create(self, serializer):
        """
        Create a new order linked to the authenticated customer.
        Also triggers an SMS notification via the `send_sms` signal.
        """
        customer = Customer.objects.get(user=self.request.user)
        order = serializer.save(customer=customer)

        from .signals import send_sms
        message = f"Dear {customer.name}, your order #{order.id} has been placed."
        send_sms(customer.phone_number, message)


class TransactionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Transactions.
    Provides CRUD operations for order-related transactions.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
