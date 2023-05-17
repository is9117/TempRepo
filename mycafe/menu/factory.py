# -*- coding: utf-8 -*-

from django.utils import timezone

import factory

from menu.models import Product

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
    
    category = factory.Faker('word')
    price = factory.Faker('random_int')
    cost = factory.Faker('random_int')
    name = factory.Faker('name')
    description = factory.Faker('sentence')
    barcode = factory.Faker('word')
    expiration_date = factory.Faker('date')
    size = factory.Iterator(('S', 'L'))
