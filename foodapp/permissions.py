from rest_framework.permissions import BasePermission


# login and registractions

class AdminPermission(BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.role == 'admin')


class BoyProfilePermissions(BasePermission):

    def has_permission(self, request, view):
        if request.user.role == 'admin':
            return request.method == 'GET'

        if request.user.role == 'delivery_boy':
            return request.method in [
                'GET', 'POST', 'PUT', 'PATCH', 'DELETE'
            ]

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return request.method == 'GET'

        if request.user.role == 'delivery_boy':
            return obj.owner == request.user

        return False


class PartnerProfilePermissions(BasePermission):

        def has_permission(self, request, view):
            if request.user.role == 'admin':
              return request.method == 'GET'

            if request.user.role == 'resturent_partner':
                return request.method in [
                    'GET', 'POST', 'PUT', 'PATCH', 'DELETE'
                            ]

            return False

        def has_object_permission(self, request, view, obj):
            if request.user.role == 'admin':
                return request.method == 'GET'

            if request.user.role == 'resturent_partner':
                return obj.owner == request.user

            return False

    
