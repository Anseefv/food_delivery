from django.shortcuts import render
from rest_framework.generics import *
from .serializers import *
from .models import *
from rest_framework.authentication import TokenAuthentication
from .permissions import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError


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


# resturent  and branches

class ResturentViewSet(ModelViewSet):

    authentication_classes=[TokenAuthentication]
    serializer_class=ResturentSerializer
    permission_classes=[IsAuthenticated,ResturentPermissions]


    def get_queryset(self):
        

        if self.request.user.role=='admin':
            return Resturent.objects.all()
        
        if self.request.user.role=='resturent_partner':
            if self.request.method=='GET':
                return Resturent.objects.all()
            
            data=Resturent_PartnerProfile.objects.filter(owner=self.request.user).first()
            if not data:
                raise ValidationError("partner must be partner_profile")
            
            return Resturent.objects.filter(owner=data)

        return None

    def perform_create(self, serializer):

        data=Resturent_PartnerProfile.objects.filter(owner=self.request.user).first()
        if not data:
            raise ValidationError("partner must be partner_profile")

        if Resturent.objects.filter(owner=data).exists():
            raise ValidationError("already exist")

        return serializer.save(owner=data)


class ResturentBranchViewset(ModelViewSet):

    authentication_classes=[TokenAuthentication]
    serializer_class=ResturentBranchSerializer
    permission_classes=[IsAuthenticated,BranchPermissions]

    def get_queryset(self):

        if self.request.user.role=='admin':
            return ResturentBranches.objects.all()

        if self.request.user.role=='resturent_partner':
            if self.request.method=='GET':
                return ResturentBranches.objects.all()
        
        return ResturentBranches.objects.filter(main_resturent__owner__owner=self.request.user)

    
    def perform_create(self, serializer):

        data=Resturent.objects.filter(owner__owner=self.request.user).first()
        if not data:
            raise ValidationError("register main resturent")

        return serializer.save(main_resturent=data)
       

    