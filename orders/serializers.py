from rest_framework import serializers
from django.db import transaction
from .models import Customer, Inventory, Order, OrderItem


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'code', 'phone_number']


class InventorySerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Inventory
        fields = ['id', 'name', 'on_hand', 'warn_limit', 'created_at', 'status']

    def get_status(self, obj):
        return obj.get_status()


class OrderItemSerializer(serializers.ModelSerializer):
    # Show full inventory details when reading
    inventory = InventorySerializer(read_only=True)
    # Accept inventory_id when writing
    inventory_id = serializers.PrimaryKeyRelatedField(
        queryset=Inventory.objects.all(),
        source="inventory",
        write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'inventory', 'inventory_id', 'quantity', 'price_at_order']
        read_only_fields = ['price_at_order']  # auto-set, not user input


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'state', 'created_at', 'items']

    def validate(self, data):
        """
        Ensure items don’t exceed available stock (if not draft).
        """
        items = self.initial_data.get("items", [])
        state = data.get("state", "DRAFT")

        if state != "DRAFT":
            for item in items:
                inventory = Inventory.objects.get(pk=item["inventory_id"])
                if item["quantity"] > inventory.on_hand:
                    raise serializers.ValidationError(
                        f"Not enough stock for {inventory.name} (available {inventory.on_hand})"
                    )
        return data

    def create(self, validated_data):
        items_data = validated_data.pop('items')

        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            for item_data in items_data:
                inventory = item_data['inventory']
                OrderItem.objects.create(
                    order=order,
                    inventory=inventory,
                    quantity=item_data['quantity'],
                    price_at_order=inventory.price if hasattr(inventory, 'price') else 0  # adjust if you have price field
                )
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)

        with transaction.atomic():
            instance.customer = validated_data.get('customer', instance.customer)
            instance.state = validated_data.get('state', instance.state)
            instance.save()

            if items_data is not None:
                instance.items.all().delete()  # Clear existing items
                for item_data in items_data:
                    inventory = item_data['inventory']
                    OrderItem.objects.create(
                        order=instance,
                        inventory=inventory,
                        quantity=item_data['quantity'],
                        price_at_order=inventory.price if hasattr(inventory, 'price') else 0
                    )
        return instance
