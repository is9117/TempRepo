# -*- coding: utf-8 -*-

from django.urls import path
from menu import views

urlpatterns = [
    path('products', views.ProductListCreateView.as_view()),
    path('products/<int:pk>', views.ProductRetrieveUpdateDestroyView.as_view()),
]
