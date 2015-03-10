from django.db import models


class Futures(models.Model):
    name = models.CharField(max_length=20)
    underlying = models.ForeignKey('product.Product')
