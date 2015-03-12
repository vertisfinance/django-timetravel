from django.db import models


class Futures(models.Model):
    name = models.CharField(max_length=20)
    ticker = models.CharField(max_length=20, primary_key=True)
    underlying = models.ForeignKey('product.Product')

    def __unicode__(self):
        return 'futures %s, und: %s' % (self.ticker, self.underlying_id)
