from rest_framework.permissions import BasePermission


class IsWarehouseManager(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.managed_warehouse.exists()
        )