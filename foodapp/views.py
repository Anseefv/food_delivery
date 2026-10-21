from django.shortcuts import render
from rest_framework.generics import *
from .serializers import *
from .models import *
from rest_framework.authentication import TokenAuthentication
from .permissions import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

# Create your views here.
# login and registractions
class CustomerRegister(CreateAPIView):

    serializer_class=RegisterSerializer


class DeliveryBoyRegister(CreateAPIView):

    serializer_class=RegisterSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[AdminPermission]


    def perform_create(self, serializer):
        return serializer.save(role='delivery_boy')


class ResturentPartnerRegister(CreateAPIView):

    serializer_class=RegisterSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[AdminPermission]


    def perform_create(self, serializer):
        return serializer.save(role='resturent_partner')



class BoyProfileViewSet(ModelViewSet):

    serializer_class=BoyProfileSerializer
    authentication_classes=[TokenAuthentication]
    
    permission_classes=[IsAuthenticated,BoyProfilePermissions]


    def get_queryset(self):

        if self.request.user.role=='admin':
            return DeliveryBoyProfile.objects.all()
        if self.request.user.role=='delivery_boy':
            return DeliveryBoyProfile.objects.filter(owner=self.request.user)

        return None

    def perform_create(self, serializer):
            if DeliveryBoyProfile.objects.filter(owner=self.request.user).exists():
                raise ValidationError({
                                        "detail": "You already have a delivery boy profile."
                                        })
            return serializer.save(owner=self.request.user)

class PartnerProfileViewSet(ModelViewSet):

    serializer_class=PartnerProfileSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated,PartnerProfilePermissions]


    def get_queryset(self):

        if self.request.user.role=='admin':
            return Resturent_PartnerProfile.objects.all()
        
        if self.request.user.role=='resturent_partner':
            return Resturent_PartnerProfile.objects.filter(owner=self.request.user)

        return None

    def perform_create(self, serializer):
            if Resturent_PartnerProfile.objects.filter(owner=self.request.user).exists():
                raise ValidationError({
                                        "detail": "You already have a restaurant partner profile."
                                        })
            return serializer.save(owner=self.request.user)

