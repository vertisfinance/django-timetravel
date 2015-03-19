import os
import sys
import time

import django
from django.db import transaction


os.environ['DJANGO_SETTINGS_MODULE'] = 'project1.settings'
thisdir = os.path.split(__file__)[0]
path = os.path.abspath(os.path.join(thisdir, '../project1'))
sys.path.insert(0, path)


django.setup()


from product.models import Product
from django.contrib.auth.models import User
from django.core.management import call_command

from django_timetravel import timetravel, to_decimal


call_command('flush', interactive=False, verbosity=0)


with transaction.atomic():
    alice = User.objects.create_user('alice', password='alice')
    bob = User.objects.create_user('bob', password='bob')
    charlie = User.objects.create_user('charlie', password='charlie')

p = Product(name='a', price=1)
p.save()

t1 = to_decimal(time.time())

p.price = 2
p.maintainers.add(alice, bob)
p.save()

t2 = to_decimal(time.time())


def print_product(p):
    print p
    for m in p.maintainers.all():
        print '    %s' % m


print 't1'
with timetravel(t1):
    p = Product.objects.get(name='a')
    print_product(p)
    p = alice.products.all()
    print p


print 't2'
with timetravel(t2):
    p = Product.objects.get(name='a')
    print_product(p)

    p = alice.products.all()
    print p
