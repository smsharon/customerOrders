# orders/serializers.py
from rest_framework import serializers
from .models import Customer, Inventory, Order, OrderItem, Transaction


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'code', 'phone_number']


class InventorySerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Inventory
        fields = ['id', 'name', 'on_hand', 'warn_limit', 'status']

    def get_status(self, obj):
        return obj.get_status()


class OrderItemSerializer(serializers.ModelSerializer):
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
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'state', 'created_at', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item in items_data:
            OrderItem.objects.create(order=order, **item)

        return order


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'order', 'customer', 'action', 'description', 'timestamp']
