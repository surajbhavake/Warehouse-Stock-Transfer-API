from django.db import transaction

from .models import(
    Stock,
    StockTransfer,
    AuditLog
)

def transfer_stock(
        *,
        user,
        product,
        source_warehouse,
        destination_warehouse,
        quantity,
):
    if source_warehouse == destination_warehouse:
        raise ValueError(
            'Source and destination warehouse must be different'
        )

    if source_warehouse.manager != user:
        raise PermissionError(
            'You do not manage the source Warehouse'
        )

    with transaction.atomic:

        source_stock = Stock.objects.get(
            product = product,
            warehouse = source_warehouse,
        )
        destination_stock = Stock.objects.get_or_create(
            product = product,
            warehouse = destination_warehouse,
        )

        if source_stock.quantity < quantity:
            raise ValueError(
                'Not enough stock available'
            )

        source_stock.quantity -= quantity
        destination_stock.quantity +=quantity

        source_stock.save()
        destination_stock.save()

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