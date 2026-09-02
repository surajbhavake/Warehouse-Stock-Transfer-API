from rest_framework import serializers

from .models import Product,Warehouse,Stock,StockTransfer


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
    