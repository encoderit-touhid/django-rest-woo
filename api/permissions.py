from rest_framework.permissions import BasePermission


class IsSelfOrder(BasePermission):
    """
    Allow access only to the user who owns the order.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.user == request.user