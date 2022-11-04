# Generated by Django 4.1.2 on 2022-11-04 11:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("shopplyapp", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="product",
        ),
        migrations.RemoveField(
            model_name="order",
            name="quantity",
        ),
        migrations.RemoveField(
            model_name="product",
            name="quantity",
        ),
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("Payment pending", "Pending Payment"),
                    ("Paid", "Paid"),
                    ("Delivery", "In Delivery"),
                    ("Delivered", "Delivered"),
                    ("Cancelled", "Cancelled"),
                ],
                default="Payment pending",
                max_length=20,
            ),
        ),
        migrations.CreateModel(
            name="Stock",
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
                ("quantity", models.IntegerField(default=0)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="shopplyapp.product",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductBatch",
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
                ("quantity", models.IntegerField(default=0)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("reserved", "Reserved"),
                            ("sold", "Sold"),
                            ("released", "Released"),
                        ],
                        default="reserved",
                        max_length=20,
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="shopplyapp.order",
                    ),
                ),
                (
                    "sku",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="shopplyapp.stock",
                    ),
                ),
            ],
        ),
    ]
