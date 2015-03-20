from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=20, primary_key=True)

    def __unicode__(self):
        return self.name


class Forward(Product):
    underlying = models.ForeignKey(Product, related_name='underlying_for')
    expiry = models.DateField()


class Futures(Forward):
    clearer = models.ForeignKey('client.Clearer', db_column='clearer_client')
