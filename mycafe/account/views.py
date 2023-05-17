# -*- coding: utf-8 -*-

from rest_framework import views, generics
from rest_framework import exceptions, status
from rest_framework.response import Response

from account import models, serializers
from mycafe.responses import CustomResponse
from mycafe.jwt import create_token

class AccountCreateView(generics.CreateAPIView):
    serializer_class = serializers.AccountSerializer
    queryset = models.Account.objects

    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code == 201:
            response = CustomResponse(data=response.data, status=status.HTTP_201_CREATED, *args, **kwargs)
        return super().finalize_response(request, response, *args, **kwargs)

class TokenCreateDeleteView(views.APIView):

    def post(self, request, *args, **kwargs):
        serializer = serializers.AccountSerializer(data=request.data)
        if not serializer.is_valid():
            raise exceptions.ParseError(serializer.errors)
        
        try:
            inst = models.Account.objects.get(phone_num=serializer.validated_data['phone_num'])
        except models.Account.DoesNotExist:
            raise exceptions.NotFound
        
        if not inst.check_password(serializer.validated_data['password']):
            raise exceptions.ParseError({'password': 'invalid'})
        
        token = create_token(inst.id)

        return CustomResponse(data=token, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):

        if not request.auth:
            raise exceptions.NotAuthenticated
        
        serializer = serializers.TokenSerializer(data=request.data)
        if not serializer.is_valid():
            raise exceptions.ParseError(serializer.errors)
        
        token = serializer.validated_data['token']

        models.InvalidatedToken.objects.get_or_create(token=token)
        
        return CustomResponse(status=status.HTTP_204_NO_CONTENT)
