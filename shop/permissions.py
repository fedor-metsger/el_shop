
from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):

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