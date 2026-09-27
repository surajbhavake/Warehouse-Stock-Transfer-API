from django.urls import path
from .views import StockTransferView,BatchListCreateView,AddBatchStockView

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
]