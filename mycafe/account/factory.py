# -*- coding: utf-8 -*-

from django.utils import timezone

import faker
import factory

from account.models import Account

class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Account

    plaintext_password = factory.PostGenerationMethodCall(
                            'set_password', 'defaultpassword')
    
    @factory.lazy_attribute
    def phone_num(self):
        phone_num_stub = ''.join([str(faker.Faker().random_digit()) for _ in range(8)])
        return f'010{phone_num_stub}'
