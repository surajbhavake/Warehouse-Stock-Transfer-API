from django.urls import path
from .views import (
    StockTransferView,BatchListCreateView,AddBatchStockView,

    ProductListCreateView,
    ProductDetailView,
    ProductUpdateView,

    WarehouseListCreateView,
    WarehouseDetailView,
    WarehouseUpdateView,
)
urlpatterns = [

    # ============================================
    # PRODUCTS
    # ============================================

    path(
        'products/',
        ProductListCreateView.as_view(),
        name='product-list-create'
    ),

    path(
        'products/<int:pk>/',
        ProductDetailView.as_view(),
        name='product-detail'
    ),

    path(
        'products/<int:pk>/update/',
        ProductUpdateView.as_view(),
        name='product-update'
    ),


    # ============================================
    # WAREHOUSES
    # ============================================

    path(
        'warehouses/',
        WarehouseListCreateView.as_view(),
        name='warehouse-list-create'
    ),

    path(
        'warehouses/<int:pk>/',
        WarehouseDetailView.as_view(),
        name='warehouse-detail'
    ),

    path(
        'warehouses/<int:pk>/update/',
        WarehouseUpdateView.as_view(),
        name='warehouse-update'
    ),


    # ============================================
    # STOCK TRANSFER
    # ============================================

    path(
        'transfers/',
        StockTransferView.as_view(),
        name='stock-transfer'
    ),


    # ============================================
    # BATCHES
    # ============================================

    path(
        'batches/',
        BatchListCreateView.as_view(),
        name='batch-list-create'
    ),


    # ============================================
    # BATCH STOCK
    # ============================================

    path(
        'batch-stock/',
        AddBatchStockView.as_view(),
        name='add-batch-stock'
    ),
]