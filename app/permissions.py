from rest_framework.permissions import (
    BasePermission, 
    SAFE_METHODS,
    )

class IsOrderOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and (obj.user == request.user or request.user.is_staff)

        
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user != 'AnonymousUser':
            if request.user.is_superuser or request.user.role == 'admin':
                return True