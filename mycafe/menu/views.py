# -*- coding: utf-8 -*-

from rest_framework import generics

from menu import serializers
from menu import models
from mycafe.permissions import IsAuthenticated
from mycafe.responses import CustomResponse


def is_chosung(string):
    # 초성 리스트. 00 ~ 18
    CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    for char in string:
        if char not in CHOSUNG_LIST:
            return False
    return True

class ProductListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ProductSerislizer
    queryset = models.Product.objects.all()

    def filter_queryset(self, queryset):
        query_params = self.request.query_params
        if query := query_params.get('query'):
            if is_chosung(query):
                queryset = queryset.filter(name_chosungs__icontains=query)
            else:
                queryset = queryset.filter(name__icontains=query)
        return super().filter_queryset(queryset)
    
    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code in (201, 200):
            response = CustomResponse(data=response.data, status=response.status_code, *args, **kwargs)
        return super().finalize_response(request, response, *args, **kwargs)

class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ProductSerislizer
    queryset = models.Product.objects

    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code in (200, 204):
            response = CustomResponse(data=response.data, status=response.status_code, *args, **kwargs)
        return super().finalize_response(request, response, *args, **kwargs)

