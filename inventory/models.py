from django.db import models
from django.conf import settings

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=50,unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name




class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)

    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='managed_warehouse',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name



class Stock(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='stock_records'
    )

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name='stock_records'
    )

    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product','warehouse'],
                name = 'unique_product_warehouse_stock'
            )
        ]

    def __str__(self):
        return f"{self.product} - {self.warehouse}"



class StockTransfer(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='transfers'
    )
    source_warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        related_name='outgoing_transfers'
    )

    destination_warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        related_name='incoming_transfers'
    )

    quantity = models.PositiveIntegerField()

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='stock_transfer'
    )

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):

        return(
            f'{self.product}- {self.source_warehouse}  - {self.destination_warehouse}'
        )


class AuditLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="audit_logs"
    )

    action = models.CharField(max_length=100)

    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action}"


class Batch(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='batches'
    )
    batch_number = models.CharField(
        max_length=100
    )
    manufacturing_date = models.DateField()
    expiry_date = models.DateField()
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product','batch_number'],
                name='unique_product_batch_number'
            )
        ]

    def __str__(self):
        return f"{self.product.name} - {self.batch_number}"



class BatchStock(models.Model):
    batch = models.ForeignKey(
        Batch,
        on_delete=models.PROTECT,
        related_name='stock_records'
    )

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        related_name='batch_stock_records'
    )
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        constraints =[
            models.UniqueConstraint(
                fields=['batch','warehouse'],
                name='unique_batch_warehouse_stock'
            )
        ]

    def __str__(self):
        return (
            f'{self.batch}-'
            f'{self.warehouse}-'
            f'{self.quantity}'
        )