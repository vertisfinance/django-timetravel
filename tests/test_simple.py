def test_simple():
    from product.models import Product

    prod = Product(name='testproduct', price=5.67)
    prod.save()
