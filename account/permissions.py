from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from account.models import Account


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsVendor(IsAuthenticated):
    def has_permission(self, request, views):
        is_authenticated = super().has_permission(request, views)
        user = Account.objects.get(user=request.user)
        if not is_authenticated:
            return False

        return user.is_vendor


class AnonPermissionOnly(permissions.BasePermission):
    message = 'You are already authenticated'

    def has_permission(self, request, view):
        return not request.user.is_authenticated

