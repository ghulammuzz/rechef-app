from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class isUserLogin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated or not request.user:
            raise PermissionDenied({"message": "Harap Login Terlebih Dahulu"})
        return True