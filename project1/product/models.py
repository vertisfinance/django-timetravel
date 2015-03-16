from django.db import models
from notinst.models import NI


NI()


class Product(models.Model):
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    maintainers = models.ManyToManyField('auth.User')

    def __unicode__(self):
        return 'product %s, price: %s' % (self.name, self.price)
