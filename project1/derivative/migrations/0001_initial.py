# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Futures',
            fields=[
                ('name', models.CharField(max_length=20)),
                ('ticker', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('underlying', models.ForeignKey(to='product.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
