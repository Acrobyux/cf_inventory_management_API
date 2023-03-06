from django.db import models
from rest_framework.exceptions import ValidationError

from .constants import *


# Create your models here.
class Warehouse(models.Model):
    """
    Represents a warehouse where products can be stored.
    """

    name = models.CharField(max_length=100, help_text="Name of the warehouse.")
    address = models.CharField(max_length=200, help_text="Address of the warehouse.")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=ACTIVE, help_text="Status of the warehouse.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Creation date of the warehouse.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Last update date of the warehouse.")

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Represents a category that a product can belong to.
    """
    name = models.CharField(max_length=100, help_text="Name of the category.")
    description = models.CharField(max_length=200, blank=True, help_text="Description of the category.")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=ACTIVE, help_text="Status of the Category.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Creation date of the category.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Last update date of the category.")

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Represents a product that can be stored in a warehouse.
    """
    name = models.CharField(max_length=100, help_text="Name of the product.")
    description = models.CharField(max_length=200, blank=True, help_text="Description of the product.")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, help_text="Category of the product.")
    status = models.CharField(max_length=10, default=ACTIVE, help_text="Status of the product.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Creation date of the product.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Last update date of the product.")

    def __str__(self):
        return self.name


class Inventory(models.Model):
    """
    Represents the inventory of a product in a specific warehouse.
    """
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, help_text="Warehouse of the inventory.")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, help_text="Product of the inventory.")
    quantity = models.IntegerField(default=0, help_text="Quantity of the product in the warehouse.")

    def __str__(self):
        return f"{self.product.name} ({self.quantity}) at {self.warehouse.name}"


class Movement(models.Model):
    """
    Represents a movement of a product between warehouses or a change in the quantity of a product in a warehouse.
    """
    IN = 'IN'
    OUT = 'OUT'
    TRANSFER = 'TRANSFER'
    MOVEMENT_TYPES = [
        (IN, 'In'),
        (OUT, 'Out'),
        (TRANSFER, 'Transfer'),
    ]

    movement_type = models.CharField(max_length=10, choices=MOVEMENT_TYPES, help_text="Type of the movement.")
    warehouse_from = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='movements_from', null=True,
                                       blank=True, help_text="Warehouse of the movement (for OUT and TRANSFER types).")
    warehouse_to = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='movements_to', null=True,
                                     blank=True, help_text="Warehouse of the movement (for IN and TRANSFER types).")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, help_text="Product of the movement.")
    quantity = models.IntegerField(default=0, help_text="Quantity of the product in the movement.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Creation date of the movement.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Last update date of the movement.")

    def __str__(self):
        return f"{self.movement_type} {self.quantity} {self.product.name}"
