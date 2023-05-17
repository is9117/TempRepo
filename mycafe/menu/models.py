from django.db import models

class Product(models.Model):

    class Meta:
        ordering = ('-id',)

    SIZE_CHOICES = (
        ('S', 'small'),
        ('L', 'large')
    )

    category = models.CharField(max_length=16, null=True, blank=True)
    price = models.IntegerField(default=0)
    cost = models.IntegerField(default=0)
    name = models.CharField(max_length=128, null=True, blank=True)
    name_chosungs = models.CharField(max_length=128, null=True, blank=True)
    description = models.CharField(max_length=1024, null=True, blank=True)
    barcode = models.CharField(max_length=128, null=True, blank=True)
    expiration_date = models.DateField(null=True)
    size = models.CharField(max_length=1, choices=SIZE_CHOICES)
