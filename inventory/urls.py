from django.urls import path
from .views import StockTransferView

urlpatterns = [
    path(
        'transfers/',StockTransferView.as_view(),name='stock-transfer',
    ),
]