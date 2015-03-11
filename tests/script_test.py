import sys
import os
import os.path as p

import django

project_path = p.abspath(p.join(p.dirname(__file__), '../test_project'))
sys.path.insert(0, project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'test_project.settings'
django.setup()

from product.models import Product


prod1 = Product(name='apple', price=3.141593)
prod2 = Product(name='pear', price=2.718282)
# prod.save()
# prod.price = 2.718282
# prod.save()
Product.objects.bulk_create((prod1, prod2))

print 'queries num: %s' % len(django.db.connection.queries)
