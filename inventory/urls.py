from django.urls import path
from .views import (
    StockTransferView,BatchListCreateView,AddBatchStockView,
    ProductListCreateView,
    WarehouseListCreateView,
)
urlpatterns = [
    path(
        'transfers/',StockTransferView.as_view(),name='stock-transfer',
    ),
     path(
        'batches/',
        BatchListCreateView.as_view(),
        name='batch-list-create'
    ),
    path(
    'batch-stock/',
    AddBatchStockView.as_view(),
    name='add-batch-stock'
    ),
    path(
        'products/',
        ProductListCreateView.as_view(),
        name = 'product-list-create'
    ),
    path(
        'warehouses/',
        WarehouseListCreateView.as_view(),
        name='warehouse-list-create'
    )

]