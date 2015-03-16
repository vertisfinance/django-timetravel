import os
import sys
import time

import django
from django.db import connection
from django.db import transaction


os.environ['DJANGO_SETTINGS_MODULE'] = 'project1.settings'
thisdir = os.path.split(__file__)[0]
path = os.path.abspath(os.path.join(thisdir, '../project1'))
sys.path.insert(0, path)


django.setup()


from product.models import Product


p = Product(name='x', price=1)
p.save()


with transaction.atomic():
    p = Product(name='y', price=1)
    p.save()
    p.price = 2
    p.save()
    p.delete()


with transaction.atomic():
    p = Product(name='z', price=1)
    p.save()
    p.price = 2
    p.save()
    p.price = 3
    p.save()

# def get_now():
#     cur = connection.cursor()
#     cur.execute('SELECT now()')
#     now = cur.fetchone()[0]
#     print now


# def get_autocommit():
#     print 'autocommit is %s' % connection.get_autocommit()


# get_autocommit()

# with transaction.atomic():
#     get_autocommit()
#     get_now()
#     time.sleep(0.5)
#     get_now()
#     p = Product(name='x', price=1)
#     p.save()
#     time.sleep(0.5)
#     get_now()
#     time.sleep(0.5)
#     prods = list(Product.objects.all())
#     get_now()
#     get_autocommit()


# get_autocommit()

# with transaction.atomic():
#     get_autocommit()
#     get_now()

# get_autocommit()


# for q in connection.queries:
#     print q['sql']
