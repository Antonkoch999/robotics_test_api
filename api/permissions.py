from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsAdministrator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='administrator'):
            return True
        return False


class IsDealer(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='dealer'):
            return True
        return False


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='user'):
            return True
        return False
