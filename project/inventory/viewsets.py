from rest_framework import viewsets, status
from rest_framework.response import Response
from .constants import *
from .serializers import *
from .models import *
from .pagination import BasePagination


# Manage simple CRUD operations for warehouses, categories and products
class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    pagination_class = BasePagination


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = BasePagination


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    pagination_class = BasePagination

    def get_serializer_class(self):
        if self.action in ['list']:
            return ProductListSerializer
        return ProductSerializer


# Read-only viewset for inventory (stock) because it's not supposed to be modified directly from the client
# It's updated automatically when a movement is created or updated
class InventoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Inventory.objects.all()
    pagination_class = BasePagination

    def get_serializer_class(self):
        if self.action in ['list']:
            return InventoryListSerializer
        return InventorySerializer

    # Deny creation of new inventories
    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # Deny update of inventories
    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # Deny delete of inventories
    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


# Manage inventory movements (in, out and transfer)
#     - In: add stock to a warehouse
#     - Out: remove stock from a warehouse
#     - Transfer: move stock from one warehouse to another
class MovementViewSet(viewsets.ModelViewSet):
    queryset = Movement.objects.all()
    pagination_class = BasePagination

    def get_serializer_class(self):
        if self.action in ['list']:
            return MovementListSerializer
        return MovementSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        movement_type = serializer.validated_data['movement_type'].upper()
        quantity = serializer.validated_data['quantity']
        warehouse_to = serializer.validated_data.get('warehouse_to')
        warehouse_from = serializer.validated_data.get('warehouse_from')
        product = serializer.validated_data['product']
        # Perform different actions based on movement_type
        if movement_type == IN:
            if not warehouse_to:
                return Response({"detail": "warehouse_to is required for In movement type"},
                                status=status.HTTP_400_BAD_REQUEST)
            if warehouse_from:
                return Response({"detail": "warehouse_from should be empty for In movement type"},
                                status=status.HTTP_400_BAD_REQUEST)
            # Check if product and warehouse exist in inventory
            try:
                inventory = Inventory.objects.get(product=product, warehouse=warehouse_to)
            except Inventory.DoesNotExist:
                inventory = Inventory.objects.create(product=product, warehouse=warehouse_to, quantity=0)
            # Create or update inventory
            inventory.quantity += quantity
            inventory.save(update_fields=['quantity'])

            # Create movement
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif movement_type == OUT:
            if not warehouse_from:
                return Response({"detail": "warehouse_from is required for Out movement type"},
                                status=status.HTTP_400_BAD_REQUEST)
            if warehouse_to:
                return Response({"detail": "warehouse_to should be empty for Out movement type"},
                                status=status.HTTP_400_BAD_REQUEST)
            # Check if product and warehouse exist in inventory
            try:
                inventory = Inventory.objects.get(product=product, warehouse=warehouse_from)
            except Inventory.DoesNotExist:
                inventory = Inventory.objects.create(product=product, warehouse=warehouse_from, quantity=0)

            # Check if there's enough stock
            if inventory.quantity < quantity:
                return Response({"detail": "There is not enough stock in the inventory."},
                                status=status.HTTP_400_BAD_REQUEST)

            # Update inventory
            inventory.quantity -= quantity
            inventory.save(update_fields=['quantity'])

            # Create movement
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif movement_type == TRANSFER:
            if not warehouse_from or not warehouse_to:
                return Response(
                    {"detail": "Both warehouse_from and warehouse_to are required for Transfer movement type"},
                    status=status.HTTP_400_BAD_REQUEST)
            if warehouse_from == warehouse_to:
                return Response({"detail": "The warehouses should be different for Transfer movement type"},
                                status=status.HTTP_400_BAD_REQUEST)
            # Check if product and warehouse exist in inventory
            try:
                inventory_from = Inventory.objects.get(product=product, warehouse=warehouse_from)
            except Inventory.DoesNotExist:
                inventory_from = Inventory.objects.create(product=product, warehouse=warehouse_from, quantity=0)

            # Check if there's enough stock in the origin inventory
            if inventory_from.quantity < quantity:
                return Response({"detail": "There is not enough stock in the inventory."},
                                status=status.HTTP_400_BAD_REQUEST)

            # Check if the destination inventory exists
            try:
                inventory_to = Inventory.objects.get(warehouse=warehouse_to, product=product)
            except Inventory.DoesNotExist:
                inventory_to = Inventory.objects.create(product=product, warehouse=warehouse_to, quantity=0)

            # Update inventories
            inventory_from.quantity -= quantity
            inventory_to.quantity += quantity
            inventory_from.save(update_fields=['quantity'])
            inventory_to.save(update_fields=['quantity'])

            # Create movement
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        # get product and warehouse from movement
        product = instance.product
        warehouse = instance.warehouse_to or instance.warehouse_from

        # get inventory for the product and warehouse
        inventory = Inventory.objects.get(product=product, warehouse=warehouse)

        # update inventory quantity based on movement type
        if instance.movement_type == IN:
            inventory.quantity -= instance.quantity
        elif instance.movement_type == OUT:
            inventory.quantity += instance.quantity
        elif instance.movement_type == TRANSFER:
            inventory.quantity += instance.quantity
            inventory_to = Inventory.objects.get(product=product, warehouse=instance.warehouse_to)
            inventory_to.quantity -= instance.quantity

        # save updated inventory
        inventory.save()

        # delete movement instance
        instance.delete()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        movement_type = serializer.validated_data.get('movement_type', instance.movement_type).upper()
        quantity = serializer.validated_data.get('quantity', instance.quantity)
        warehouse_to = serializer.validated_data.get('warehouse_to', instance.warehouse_to)
        warehouse_from = serializer.validated_data.get('warehouse_from', instance.warehouse_from)
        product = serializer.validated_data.get('product', instance.product)

        # Perform different actions based on movement_type
        if movement_type == IN:
            if warehouse_from:
                return Response({"detail": "warehouse_from should be empty for In movement type"},
                                status=status.HTTP_400_BAD_REQUEST)
            if not warehouse_to:
                warehouse_to = instance.warehouse_to

            # Check if product and warehouse exist in inventory
            try:
                inventory = Inventory.objects.get(product=product, warehouse=warehouse_to)
            except Inventory.DoesNotExist:
                inventory = Inventory.objects.create(product=product, warehouse=warehouse_to, quantity=0)

            # Update inventory
            inventory.quantity += quantity - instance.quantity
            inventory.save(update_fields=['quantity'])

            # Update movement
            serializer.save()

            return Response(serializer.data)
        elif movement_type == OUT:
            if warehouse_to:
                return Response({"detail": "warehouse_to should be empty for Out movement type"},
                                status=status.HTTP_400_BAD_REQUEST)
            if not warehouse_from:
                warehouse_from = instance.warehouse_from

            # Check if product and warehouse exist in inventory
            try:
                inventory = Inventory.objects.get(product=product, warehouse=warehouse_from)
            except Inventory.DoesNotExist:
                inventory = Inventory.objects.create(product=product, warehouse=warehouse_from, quantity=0)

            # Check if there's enough stock
            if inventory.quantity < quantity - instance.quantity:
                return Response({"detail": "There is not enough stock in the inventory."},
                                status=status.HTTP_400_BAD_REQUEST)

            # Update inventory
            inventory.quantity -= quantity - instance.quantity
            inventory.save(update_fields=['quantity'])

            # Update movement
            serializer.save()

            return Response(serializer.data)
        elif movement_type == TRANSFER:
            if not warehouse_from or not warehouse_to:
                return Response(
                    {"detail": "Both warehouse_from and warehouse_to should be provided for Transfer movement type"},
                    status=status.HTTP_400_BAD_REQUEST)

            # Check if product and warehouses exist in inventory
            try:
                inventory_from = Inventory.objects.get(product=product, warehouse=warehouse_from)
            except Inventory.DoesNotExist:
                return Response(
                    {"detail": f"Product {product.name} does not exist in warehouse {warehouse_from.name}."},
                    status=status.HTTP_400_BAD_REQUEST)
            try:
                inventory_to = Inventory.objects.get(product=product, warehouse=warehouse_to)
            except Inventory.DoesNotExist:
                inventory_to = Inventory.objects.create(product=product, warehouse=warehouse_to, quantity=0)

            # Check if there's enough stock in the source inventory
            if inventory_from.quantity < quantity:
                return Response({"detail": "There is not enough stock in the source inventory."},
                                status=status.HTTP_400_BAD_REQUEST)

            # Update inventories
            inventory_from.quantity -= quantity
            inventory_from.save(update_fields=['quantity'])

            inventory_to.quantity += quantity
            inventory_to.save(update_fields=['quantity'])

            # Update movement
            serializer.save()

            return Response(serializer.data)

