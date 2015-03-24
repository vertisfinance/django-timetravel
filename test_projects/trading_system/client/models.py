from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=100)
    signed_contracts = models.ManyToManyField('Contract')
    classification = models.CharField(max_length=1, default='A')

    def __unicode__(self):
        return self.name


class Clearer(Client):
    pass


class Contract(models.Model):
    name = models.CharField(max_length=10)
    tradable_products = models.ManyToManyField('product.Product')


# To test chained inheritance
# Funny, but this does not work as expected in django itself.
class A(models.Model):
    a = models.CharField(max_length=1, primary_key=True)


class B(models.Model):
    b = models.CharField(max_length=1, primary_key=True)


class AB(A, B):
    pass


class ClientProxy(Client):
    class Meta:
        proxy = True

    def can_trade(self):
        return True
