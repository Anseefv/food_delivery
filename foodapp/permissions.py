from rest_framework.permissions import BasePermission
from .models import Resturent_PartnerProfile,Resturent
from rest_framework.exceptions import ValidationError


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

    
# resturent  and branches


class ResturentPermissions(BasePermission):

        def has_permission(self, request, view):
            if request.user.role in ['admin','customer']:
              return request.method == 'GET'

            if request.user.role == 'resturent_partner':
                return request.method in [
                    'GET', 'POST', 'PUT', 'PATCH', 'DELETE'
                            ]

            return False

        def has_object_permission(self, request, view, obj):

            
            
            if request.user.role in ['admin','customer']:
                return request.method == 'GET'

            if request.user.role == 'resturent_partner':
                if request.method == 'GET':
                    return True
                data=Resturent_PartnerProfile.objects.filter(owner=request.user).first()
                if not data:
                    raise ValidationError("partner must be partner_profile")
                return obj.owner == data

            return False


class BranchPermissions(BasePermission):

        def has_permission(self, request, view):
            if request.user.role in ['admin','customer']:
              return request.method == 'GET'

            if request.user.role == 'resturent_partner':
                return request.method in [
                    'GET', 'POST', 'PUT', 'PATCH', 'DELETE'
                            ]

            return False

        def has_object_permission(self, request, view, obj):

            
            
            if request.user.role in ['admin','customer']:
                return request.method == 'GET'

            if request.user.role == 'resturent_partner':
                if request.method == 'GET':
                    return True
                data=Resturent.objects.filter(owner__owner=request.user).first()
                if not data:
                    raise ValidationError("register main resturent")
                return obj.main_resturent == data

            return False