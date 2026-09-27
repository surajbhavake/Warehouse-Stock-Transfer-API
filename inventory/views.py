from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    StockTransferSerializer,BatchSerializer,BatchStockSerializer,AddBatchStockSerializer
)
from .permissions import IsWarehouseManager
from .services import transfer_stock,add_batch_stock
from .models import Batch,BatchStock

# Create your views here.

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

        batches = Batch.objects.select_related('product').all

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