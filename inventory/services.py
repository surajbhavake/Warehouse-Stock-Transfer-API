from django.db import transaction
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import PermissionDenied
from .models import(
    Stock,
    StockTransfer,
    AuditLog
)
from django.core.exceptions import ObjectDoesNotExist

def transfer_stock(
        *,
        user,
        product,
        source_warehouse,
        destination_warehouse,
        quantity,
):
    if source_warehouse == destination_warehouse:
        raise ValidationError(
            'Source and destination warehouse must be different'
        )

    if source_warehouse.manager != user:
        raise PermissionDenied(
            'You do not manage the source Warehouse'
        )

    with transaction.atomic():
        try:

            source_stock = Stock.objects.select_for_update().get(
                product = product,
                warehouse = source_warehouse,
            )
        except Stock.ObjectDoesNotExist:
            raise ValidationError(
                'Source warehouse has no stock for this product'
            )

        try:
            destination_stock = Stock.objects.select_for_update().get(
                product = product,
                warehouse = destination_warehouse,
            )
        except Stock.ObjectDoesNotExist:
            destination_stock = Stock.objects.create(
                product = product,
                warehouse = destination_warehouse,
                quantity = 0,
            )
      

        if source_stock.quantity < quantity:
            raise ValidationError(
                'Not enough stock available'
            )

        source_stock.quantity -= quantity
        destination_stock.quantity +=quantity

        source_stock.save(
            update_fields=['quantity']
        )
        destination_stock.save(
            update_fields=['quantity']
        )

        transfer = StockTransfer.objects.create(
            product = product,
            source_warehouse = source_warehouse,
            destination_warehouse = destination_warehouse,
            quantity = quantity,
            created_by = user,
        )

        AuditLog.objects.create(
            user = user,
            action = 'STOCK_TRANSFER',
            description = (
                f'Transferred {quantity} units of {product.name}'
                f'from {source_warehouse.name} to {destination_warehouse.name}'
            ),
        )

    return transfer