# -*- coding: utf-8 -*-

from rest_framework.pagination import CursorPagination

class CustomCursorPagination(CursorPagination):
    page_size = 10
    ordering = '-id'