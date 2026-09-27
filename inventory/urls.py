from django.urls import path
from .views import StockTransferView,BatchListCreateView

urlpatterns = [
    path(
        'transfers/',StockTransferView.as_view(),name='stock-transfer',
    ),
     path(
        'batches/',
        BatchListCreateView.as_view(),
        name='batch-list-create'
    ),
]