# -*- coding: utf-8 -*-

import re

from rest_framework import serializers

from hangul_utils import split_syllable_char

from menu import models

class ProductSerislizer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        exclude = ('name_chosungs',)

    def __to_chosungs(self, name) -> str:
        return ''.join([ split_syllable_char(c)[0] for c in name if re.match(u'[\uAC00-\uD7A3]+', c)])

    def update(self, instance, validated_data):
        if 'name' in validated_data:
            name = validated_data['name']
            instance.name_chosungs = self.__to_chosungs(name)
            instance.save(update_fields=('name_chosungs',))
        return super().update(instance, validated_data)

    def create(self, validated_data):
        inst = super().create(validated_data)
        if name := validated_data.get('name'):
            inst.name_chosungs = self.__to_chosungs(name)
            inst.save(update_fields=('name_chosungs',))
        return inst
    



