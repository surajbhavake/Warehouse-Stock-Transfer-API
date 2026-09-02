from django.template import response
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
# Create your tests here.
from django.contrib.auth import get_user_model
from django.test import TestCase

from inventory.models import (
    Product,
    StockTransfer,
    Warehouse,
    Stock,
)
from inventory.services import transfer_stock
from inventory.models import StockTransfer
from inventory.models import AuditLog
from rest_framework.exceptions import ValidationError, PermissionDenied  # <-- ADD THIS!

User = get_user_model()


class TransferStockTests(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="suraj",
            password="password123",
        )

        self.product = Product.objects.create(
            name="Paracetamol",
            sku="PARA001",
        )

        self.mumbai = Warehouse.objects.create(
            name="Mumbai",
            location="Mumbai",
            manager=self.user,
        )

        self.pune = Warehouse.objects.create(
            name="Pune",
            location="Pune",
            manager=self.user,
        )

        self.mumbai_stock = Stock.objects.create(
            product=self.product,
            warehouse=self.mumbai,
            quantity=100,
        )

        self.pune_stock = Stock.objects.create(
            product=self.product,
            warehouse=self.pune,
            quantity=20,
        )

    def test_successful_transfer(self):

        transfer = transfer_stock(
            user=self.user,
            product=self.product,
            source_warehouse=self.mumbai,
            destination_warehouse=self.pune,
            quantity=50,
        )

        self.mumbai_stock.refresh_from_db()
        self.pune_stock.refresh_from_db()
        self.assertEqual(
        self.mumbai_stock.quantity,
        50,
        )

        self.assertEqual(
        self.pune_stock.quantity,
        70,
        )
        self.assertEqual(
        transfer.quantity,
        50,
        )

        self.assertEqual(
        transfer.product,
        self.product,
        )
        

        self.assertEqual(
        StockTransfer.objects.count(),
        1,
        )

        self.assertEqual(
        AuditLog.objects.count(),
        1,
        )
    def test_insufficient_stock(self):

        with self.assertRaises(ValidationError):

            transfer_stock(
                user=self.user,
                product=self.product,
                source_warehouse=self.mumbai,
                destination_warehouse=self.pune,
                quantity=500,
            )
    def test_same_warehouse_not_allowed(self):

        with self.assertRaises(ValidationError):

            transfer_stock(
                user=self.user,
                product=self.product,
                source_warehouse=self.mumbai,
                destination_warehouse=self.mumbai,
                quantity=50,
            )
    def test_user_cannot_transfer_from_warehouse_they_do_not_manage(self):

        other_user = User.objects.create_user(
            username="rahul",
            password="password123",
        )

        with self.assertRaises(PermissionDenied):

            transfer_stock(
                user=other_user,
                product=self.product,
                source_warehouse=self.mumbai,
                destination_warehouse=self.pune,
                quantity=50,
            )


class StockTransferAPITests(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="suraj",
            password="password123",
        )

        self.product = Product.objects.create(
            name="Paracetamol",
            sku="PARA001",
        )

        self.mumbai = Warehouse.objects.create(
            name="Mumbai",
            location="Mumbai",
            manager=self.user,
        )

        self.pune = Warehouse.objects.create(
            name="Pune",
            location="Pune",
            manager=self.user,
        )

        Stock.objects.create(
            product=self.product,
            warehouse=self.mumbai,
            quantity=100,
        )

        Stock.objects.create(
            product=self.product,
            warehouse=self.pune,
            quantity=20,
        )
    def test_successful_transfer(self):

        self.client.force_authenticate(
            user=self.user
        )
        response = self.client.post(
        "/api/transfers/",
        {
            "product": self.product.id,
            "source_warehouse": self.mumbai.id,
            "destination_warehouse": self.pune.id,
            "quantity": 50,
        },
        format="json",
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(
        response.data["message"],
        "Stock transferred successfully.",
        )
        self.assertEqual(
        response.data["transfer_id"],
        1,
        )
        mumbai_stock = Stock.objects.get(
            product=self.product,
            warehouse=self.mumbai,
         )

        pune_stock = Stock.objects.get(
            product=self.product,
            warehouse=self.pune,
        )
        self.assertEqual(
            mumbai_stock.quantity,
            50,
        )

        self.assertEqual(
            pune_stock.quantity,
            70,
        )
        self.assertEqual(
            StockTransfer.objects.count(),
            1,
        )

        self.assertEqual(
            AuditLog.objects.count(),
            1,
        )
    def test_insufficient_stock(self):

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.post(
            "/api/transfers/",
            {
                "product": self.product.id,
                "source_warehouse": self.mumbai.id,
                "destination_warehouse": self.pune.id,
                "quantity": 500,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        mumbai_stock = Stock.objects.get(
            product=self.product,
            warehouse=self.mumbai,
        )

        pune_stock = Stock.objects.get(
            product=self.product,
            warehouse=self.pune,
        )

        self.assertEqual(
            mumbai_stock.quantity,
            100,
        )

        self.assertEqual(
            pune_stock.quantity,
            20,
        )
        self.assertEqual(
            StockTransfer.objects.count(),
            0,
        )

        self.assertEqual(
            AuditLog.objects.count(),
            0,
        )
        response = self.client.post(
            "/api/transfers/",
            {
                "product": self.product.id,
                "source_warehouse": self.mumbai.id,
                "destination_warehouse": self.mumbai.id,
                "quantity": 50,
            },
            format="json",
        )
        other_user = User.objects.create_user(
            username="rahul",
            password="password123",
        )
        self.client.force_authenticate(
            user=other_user
        )

    def test_unauthorized_manager(self):

        other_user = User.objects.create_user(
            username="rahul",
            password="password123",
        )

        self.client.force_authenticate(
            user=other_user
        )

        response = self.client.post(
            "/api/transfers/",
            {
                "product": self.product.id,
                "source_warehouse": self.mumbai.id,
                "destination_warehouse": self.pune.id,
                "quantity": 50,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
        response = self.client.post(
            "/api/transfers/",
            {
                "product": self.product.id,
                "source_warehouse": self.mumbai.id,
                "destination_warehouse": self.pune.id,
                "quantity": 50,
            },
            format="json",
        )