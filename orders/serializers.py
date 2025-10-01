# orders/serializers.py
from rest_framework import serializers
from .models import Customer, Inventory, Order, OrderItem, Transaction


class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Customer model.

    Provides JSON serialization and deserialization for Customer instances,
    exposing id, name, code, and phone_number fields.
    """
    class Meta:
        model = Customer
        fields = ['id', 'name', 'code', 'phone_number']


class InventorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Inventory model.

    Adds a custom 'status' field based on stock availability,
    in addition to id, name, on_hand, and warn_limit.
    """
    status = serializers.SerializerMethodField()

    class Meta:
        model = Inventory
        fields = ['id', 'name', 'on_hand', 'warn_limit', 'status']

    def get_status(self, obj):
        """
        Returns the inventory status using the model's get_status method.
        """
        return obj.get_status()


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the OrderItem model.

    Maps related Inventory by both id (write-only) and name (read-only),
    while exposing id, quantity, and price_at_order.
    """
    inventory_id = serializers.PrimaryKeyRelatedField(
        queryset=Inventory.objects.all(),
        source='inventory',
        write_only=True
    )
    inventory_name = serializers.CharField(source='inventory.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'inventory_id', 'inventory_name', 'quantity', 'price_at_order']


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.

    Includes nested OrderItemSerializer for order items.
    Provides custom creation logic to handle related order items.
    """
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'state', 'created_at', 'items']

    def create(self, validated_data):
        """
        Creates an Order instance along with its related OrderItem instances.
        """
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item in items_data:
            OrderItem.objects.create(order=order, **item)

        return order


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Transaction model.

    Exposes order, customer, action, description, and timestamp fields.
    """
    class Meta:
        model = Transaction
        fields = ['id', 'order', 'customer', 'action', 'description', 'timestamp']
