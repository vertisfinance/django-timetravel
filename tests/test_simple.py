import pytest

from product.models import Product


@pytest.mark.django_db(transaction=True)
def test_simple():
    prod = Product(name='testproduct', price=5.67)
    prod.save()
