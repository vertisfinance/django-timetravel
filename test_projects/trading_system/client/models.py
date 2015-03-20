from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Clearer(Client):
    pass
