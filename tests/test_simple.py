import pytest


DJANGO_PROJECT = 'project1'
DJANGO_SETTINGS_MODULE = 'project1.settings'
DISABLE_MIGRATIONS = False
pytestmark = pytest.mark.usefixtures('setup_test_environment')


def test_simple():
    from product.models import Product
    prod = Product(name='testproduct', price=5.67)
    prod.save()
    assert prod.pk


def test_not_exists():
    from product.models import Product
    prod = Product.objects.all()
    assert not len(prod)
