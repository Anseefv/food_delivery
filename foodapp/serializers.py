from rest_framework import serializers
from .models import *


# login and registractions

class RegisterSerializer(serializers.ModelSerializer):

    password=serializers.CharField(write_only=True)

    class Meta:

        model=CustomUser
        fields=['username','email','password']

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class BoyProfileSerializer(serializers.ModelSerializer):

    class Meta:

        model=DeliveryBoyProfile
        fields="__all__"  
        read_only_fields=['owner']

    def validate_phone(self,value):
        if len( str(value)) != 10 :
            raise serializers.ValidationError(" 10 digits ")
        return value


class PartnerProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model=Resturent_PartnerProfile      
        fields="__all__"  
        read_only_fields=['owner']


    def validate_phone(self,value):
        if len( str(value)) != 10 :
            raise serializers.ValidationError(" 10 digits ")
        return value

