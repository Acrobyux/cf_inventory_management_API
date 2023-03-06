from .models import *
from rest_framework import serializers


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = '__all__'


class InventorySerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    warehouse = WarehouseSerializer()

    class Meta:
        model = Inventory
        fields = '__all__'


class MovementSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    warehouse_to = WarehouseSerializer()
    warehouse_from = WarehouseSerializer()

    class Meta:
        model = Movement
        fields = '__all__'
