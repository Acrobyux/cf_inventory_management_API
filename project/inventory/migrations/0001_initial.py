# Generated by Django 4.1.5 on 2023-03-05 21:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(help_text="Name of the category.", max_length=100),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        help_text="Description of the category.",
                        max_length=200,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("ACTIVE", "Active"), ("INACTIVE", "Inactive")],
                        default="ACTIVE",
                        help_text="Status of the Category.",
                        max_length=10,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, help_text="Creation date of the category."
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, help_text="Last update date of the category."
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Warehouse",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Name of the warehouse.", max_length=100
                    ),
                ),
                (
                    "address",
                    models.CharField(
                        help_text="Address of the warehouse.", max_length=200
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("ACTIVE", "Active"), ("INACTIVE", "Inactive")],
                        default="ACTIVE",
                        help_text="Status of the warehouse.",
                        max_length=10,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, help_text="Creation date of the warehouse."
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, help_text="Last update date of the warehouse."
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(help_text="Name of the product.", max_length=100),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        help_text="Description of the product.",
                        max_length=200,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        default="ACTIVE",
                        help_text="Status of the product.",
                        max_length=10,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, help_text="Creation date of the product."
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, help_text="Last update date of the product."
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        help_text="Category of the product.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="inventory.category",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Movement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "movement_type",
                    models.CharField(
                        choices=[
                            ("IN", "In"),
                            ("OUT", "Out"),
                            ("TRANSFER", "Transfer"),
                        ],
                        help_text="Type of the movement.",
                        max_length=10,
                    ),
                ),
                (
                    "quantity",
                    models.IntegerField(
                        default=0, help_text="Quantity of the product in the movement."
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, help_text="Creation date of the movement."
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, help_text="Last update date of the movement."
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        help_text="Product of the movement.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.product",
                    ),
                ),
                (
                    "warehouse_from",
                    models.ForeignKey(
                        blank=True,
                        help_text="Warehouse of the movement (for OUT and TRANSFER types).",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="movements_from",
                        to="inventory.warehouse",
                    ),
                ),
                (
                    "warehouse_to",
                    models.ForeignKey(
                        blank=True,
                        help_text="Warehouse of the movement (for IN and TRANSFER types).",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="movements_to",
                        to="inventory.warehouse",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Inventory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "quantity",
                    models.IntegerField(
                        default=0, help_text="Quantity of the product in the warehouse."
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        help_text="Product of the inventory.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.product",
                    ),
                ),
                (
                    "warehouse",
                    models.ForeignKey(
                        help_text="Warehouse of the inventory.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.warehouse",
                    ),
                ),
            ],
        ),
    ]
