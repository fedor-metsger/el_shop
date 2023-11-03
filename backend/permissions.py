
from rest_framework import permissions

import backend.models


class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == "create":
            return True
        elif view.action in ["list", "retrieve"]:
            return request.user.is_authenticated
        elif view.action in ["update", "partial_update", "destroy"]:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        # if view.action == "retrieve":
        #     return True
        else:
            return obj.pk == request.user.pk


class IsShop(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.type == backend.models.USER_TYPE_SHOP


class IsActive(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_active

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
