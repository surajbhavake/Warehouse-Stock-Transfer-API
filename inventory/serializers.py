from rest_framework import serializers

from .models import Product,Warehouse,Stock,StockTransfer,Batch,BatchStock


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'sku',
            'is_active',
        ]

class WarehouseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Warehouse
        fields = [
            "id",
            "name",
            "location",
        ]


class StockSerializer(serializers.ModelSerializer):

    product = ProductSerializer(read_only=True)

    class Meta:
        model = Stock
        fields = [
            "id",
            "product",
            "warehouse",
            "quantity",
        ]



class StockTransferSerializer(serializers.Serializer):

    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(
            is_active=True
        )
    )

    source_warehouse = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all()
    )

    destination_warehouse = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all()
    )

    quantity = serializers.IntegerField()


    def validate_quantity(self,value):
        if value <= 0:
            raise serializers.ValidationError(
                'Quantity must be greater than zero'
            )
        return value

    def validate(self,attrs):

        if(
            attrs['source_warehouse'] == attrs['destination_warehouse']
        ):
            raise serializers.ValidationError(
                'Source and destination warehouses must be different'
            )

        return attrs


class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch

        fields = [
            'id',
            'product',
            'batch_number',
            'manufacturing_date',
            'expiry_date',
            'created_at',
        ]

        read_only_fields = [
            'id',
            'created_at',
        ]

    def validate(self,attrs):
        manufacturing_date = attrs['manufacturing_date']
        expiry_date = attrs['expiry_date']

        if expiry_date <= manufacturing_date:
            raise serializers.ValidationError(
                'Expiry date must be after manufacturing date'
            )
        return attrs

class BatchStockSerializer(serializers.ModelSerializer):

    batch = BatchSerializer(
        read_only=True
    )

    class Meta:
        model = BatchStock

        fields = [
            'id',
            'batch',
            'warehouse',
            'quantity',
        ]

        read_only_fields = [
            'id',
            'batch',
            'quantity',
        ]