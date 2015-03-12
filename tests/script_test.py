import sys
import os
import os.path as p

import django

project_path = p.abspath(p.join(p.dirname(__file__), '../test_project'))
sys.path.insert(0, project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'test_project.settings'
django.setup()
from django.core.management import call_command

from product.models import Product
from derivative.models import Futures


call_command('flush', interactive=False)

prod1 = Product(name='apple', price=3.141593)
prod1.save()

# prod2 = Product(name='pear', price=2.718282)
# Product.objects.bulk_create((prod1, prod2))

# prod1.price = 5
# prod1.save()
# prod1.price = 6
# prod1.save()

# prod2 = Product.objects.get_or_create(name='pear')[0]

# Product.objects.all().update(price=10)


fut1 = Futures(name='fut1', ticker='FUT1', underlying=prod1)
fut1.save()

# Futures.objects.filter(ticker='FUT1').update(ticker='FUT_1')

prod1.delete()


# fut2 = Futures(name='fut2', ticker='FUT2', underlying=prod2)
# fut3 = Futures(name='fut3', ticker='FUT3', underlying=prod2)
# Futures.objects.bulk_create((fut1, fut2, fut3))


# print 'queries num: %s' % len(django.db.connection.queries)
# for q in django.db.connection.queries:
#     print q['sql']
