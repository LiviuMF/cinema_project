from django.conf import settings
from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return False or obj.user == request.user or request.user.is_superuser


class StaticToken(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        request_token = request.headers['Authorization']
        return request_token == settings.SEAT_ENDPOINT_ACCESS_TOKEN
