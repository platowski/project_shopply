# Generated by Django 4.1.2 on 2022-11-04 15:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("shopplyapp", "0002_remove_order_product_remove_order_quantity_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="stock",
            name="id",
        ),
        migrations.AlterField(
            model_name="productbatch",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT,
                related_name="items",
                to="shopplyapp.order",
            ),
        ),
        migrations.AlterField(
            model_name="stock",
            name="product",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                primary_key=True,
                related_name="stock",
                serialize=False,
                to="shopplyapp.product",
            ),
        ),
        migrations.AddConstraint(
            model_name="stock",
            constraint=models.CheckConstraint(
                check=models.Q(("quantity__gte", "0")),
                name="stock_quantity_non_negative",
            ),
        ),
    ]
