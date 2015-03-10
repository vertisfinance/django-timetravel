from django.db import models


class NI(models.Model):
    name = models.CharField(max_length=20)
