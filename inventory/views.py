from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import StockTransferSerializer
from .permissions import IsWarehouseManager
from .services import transfer_stock

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