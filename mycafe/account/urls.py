# -*- coding: utf-8 -*-

from django.urls import path
from account import views

urlpatterns = [
    path('account', views.AccountCreateView.as_view()),
    path('token', views.TokenCreateDeleteView.as_view()),
]
