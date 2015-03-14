import sys
import os
import os.path as p

import django

project_path = p.abspath(p.join(p.dirname(__file__), '../test_project'))
sys.path.insert(0, project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'test_project.settings'
django.setup()
# from django.core.management import call_command

from django.contrib.auth.models import User
from product.models import Product
# from derivative.models import Futures

# call_command('flush', interactive=False)

prod1 = Product(name='apple', price=1)
prod1.save()

alice = User.objects.get(username='Alice')
bob = User.objects.get(username='Bob')

prod1.maintainers.add(alice)
prod1.save()

# print 'queries num: %s' % len(django.db.connection.queries)
# for q in django.db.connection.queries:
#     print q['sql']
