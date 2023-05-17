# -*- coding: utf-8 -*-

from rest_framework import serializers, exceptions
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password

from account import models


def validate_and_encode_password(password: str) -> str:
    try:
        validate_password(password)
    except exceptions.ValidationError:
        raise exceptions.ParseError
    return make_password(password)


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}
    
    phone_num = serializers.RegexField(regex='^010\d{8}$')

    def create(self, validated_data):

        if password := validated_data.get('password'):
            validated_data['password'] = validate_and_encode_password(password)

        inst, created = models.Account.objects.get_or_create(phone_num=validated_data['phone_num'])
        if not created:
            raise exceptions.ParseError
        
        inst.password = validated_data['password']
        inst.save(update_fields=('password',))

        return inst
    
class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=1024)