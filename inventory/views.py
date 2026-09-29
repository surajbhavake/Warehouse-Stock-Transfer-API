from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    StockTransferSerializer,BatchSerializer,BatchStockSerializer,AddBatchStockSerializer,
    ProductSerializer,WarehouseSerializer,
)
from .permissions import IsWarehouseManager
from .services import transfer_stock,add_batch_stock
from .models import Batch,BatchStock,Product,Warehouse

from .cache import (
    get_product_list_cache,
    set_product_list_cache,
    invalidate_product_list_cache,
    get_product_detail_cache,
    set_product_detail_cache,
    invalidate_product_detail_cache,


    get_warehouse_list_cache,
    set_warehouse_list_cache,
    invalidate_warehouse_list_cache,
    get_warehouse_detail_cache,
    set_warehouse_detail_cache,
    invalidate_warehouse_detail_cache

    
)

# Create your views here.

class ProductListCreateView(APIView):
    permission_classes = [IsWarehouseManager]

    def get(self,request):
        cached_products = get_product_list_cache()

        if cached_products is not None:
            return Response(
                cached_products,
                status=status.HTTP_200_OK
            )
        products = Product.objects.filter(
            is_active=True
        )
        serializer = ProductSerializer(
            products,
            many=True
        )
        data = serializer.data

        set_product_list_cache(data)

        return Response(
            data,
            status=status.HTTP_200_OK
        )
    def post(self,request):
        serializer = ProductSerializer(
            data = request.data
        )
        serializer.is_valid(
            raise_exception=True
        )
        product = serializer.save()
        invalidate_product_list_cache()

        return Response(
            ProductSerializer(product).data,
            status=status.HTTP_201_CREATED
        )




class ProductDetailView(APIView):
    permission_classes = [IsWarehouseManager]

    def get(self,request,pk):
        cached_product = get_product_detail_cache(pk)

        if cached_product is not None:
            print('Product detail cache hit ')
            return Response(
                cached_product,
                status=status.HTTP_200_OK
            )

        print('product detail cache miss')

        try:
            product = Product.objects.get(
                pk=pk,
                is_active=True
            )
        except Product.DoesNotExist:
            return Response(
                {'detail':'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductSerializer(product)
        data = serializer.data

        set_product_detail_cache(
            pk,
            data
        )

        return Response(
            data,
            status=status.HTTP_200_OK
        )


class ProductUpdateView(APIView):
    permission_classes = [IsWarehouseManager]

    def put (self,request,pk):
        try:
            product = Product.objects.get(
                pk=pk
            )
        except Product.DoesNotExist:
            return Response(
                {'detail':'Product not found'},
                status = status.HTTP_404_NOT_FOUND
            )

        serializer = ProductSerializer(
            product,
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )
        product = serializer.save()

        invalidate_product_list_cache()

        invalidate_product_detail_cache(pk)

        return Response(
            ProductSerializer(product).data,
            status=status.HTTP_200_OK
        )


class WarehouseDetailView(APIView):


    permission_classes = [IsWarehouseManager]
    def get(self,request,pk):

        cached_warehouse = get_warehouse_detail_cache(pk)

        if cached_warehouse is not None:
            return Response(
                cached_warehouse,
                status=status.HTTP_200_OK
            )
        try:
            warehouse = Warehouse.objects.select_related('manager').get(pk=pk)

        except Warehouse.DoesNotExist:
            return Response(
                {'detail':'Warehouse not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = WarehouseSerializer(warehouse)

        data = serializer.data

        set_warehouse_detail_cache(
            pk,
            data
            )
        return Response(
            data,
            status=status.HTTP_200_OK
        )




class WarehouseUpdateView(APIView):

    permission_classes = [IsWarehouseManager]

    def put(self,request,pk):

        try:
            warehouse = Warehouse.objects.get(pk=pk)
        except Warehouse.DoesNotExist:
                   return Response(
                       {'detail':'Warehouse not found'},
                       status=status.HTTP_404_NOT_FOUND
                   )

        serializer = WarehouseSerializer(
            warehouse,
            data=request.data
        )
        serializer.is_valid(
            raise_exception=True
        )

        warehouse = serializer.save()

        invalidate_warehouse_list_cache()

        invalidate_warehouse_detail_cache(pk)

        return Response(
            WarehouseSerializer(warehouse).data,
            status=status.HTTP_200_OK
        )










class WarehouseListCreateView(APIView):
    permission_classes = [IsWarehouseManager]

    def get(self,request):
        cached_warehouse = get_warehouse_list_cache()

        if cached_warehouse is not None:
            return Response(
                cached_warehouse,
                status = status.HTTP_200_OK
            )

        warehouse = Warehouse.objects.select_related(
            'manager'
        ).all()

        serializer = WarehouseSerializer(
            warehouse,
            many=True
        )
        data = serializer.data

        set_warehouse_list_cache(data)

        return Response(
            data,
            status=status.HTTP_200_OK
        )

    def post(self,request):

        serializer = WarehouseSerializer(
            data = request.data
        )
        serializer.is_valid(
            raise_exception=True
        )
        warehouse = serializer.save()
        invalidate_warehouse_list_cache()

        return Response(
            WarehouseSerializer(warehouse).data,
            status=status.HTTP_201_CREATED
        )

class StockTransferView(APIView):
    permission_classes = [IsWarehouseManager]


    def post(self,request):
        serializer = StockTransferSerializer(
            data = request.data
        )

        serializer.is_valid(
            raise_exception=True
        )
        
        transfer = transfer_stock(
            user = request.user,
            **serializer.validated_data
        )

        return Response(
            {
                'message' : 'Stock transferred successfully.',
                'transfer_id':transfer.id,
            },
            status = status.HTTP_201_CREATED
        )

class BatchListCreateView(APIView):
    permission_classes = [IsWarehouseManager]

    def get(self,request):

        batches = Batch.objects.select_related('product').all()

        serializer = BatchSerializer(
            batches,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self,request):
        serializer = BatchSerializer(
            data = request.data
        )

        serializer.is_valid(
            raise_exception=True
        )
        batch = serializer.save()
        return Response(
            BatchSerializer(batch).data,
            status=status.HTTP_201_CREATED
        )


class AddBatchStockView(APIView):

    permission_classes = [IsWarehouseManager]

    def post(self, request):

        serializer = AddBatchStockSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        batch_stock = add_batch_stock(
            user=request.user,
            **serializer.validated_data
        )

        response_serializer = BatchStockSerializer(
            batch_stock
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )