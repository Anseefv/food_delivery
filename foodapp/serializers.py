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



# resturent  and branches

class ResturentSerializer(serializers.ModelSerializer):

    class Meta:

        model=Resturent
        fields="__all__"
        read_only_fields=['id','owner','added_at']

    owner=serializers.StringRelatedField(read_only=True)


class ResturentBranchSerializer(serializers.ModelSerializer):

    open_time = serializers.TimeField(
        format='%I:%M %p',
        input_formats=['%I:%M %p']
    )

    closing_time = serializers.TimeField(
        format='%I:%M %p',
        input_formats=['%I:%M %p']
    )
    main_resturent=serializers.StringRelatedField(read_only=True)


    class Meta:

        model=ResturentBranches
        fields="__all__"
        read_only_fields=['id','main_resturent']    