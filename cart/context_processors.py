from decimal import Decimal
from products.models import Product


def cart_context(request):
    cart = request.session.get('cart', {})

    products = Product.objects.filter(id__in=cart.keys())

    cart_total = Decimal('0.00')
    cart_count = 0

    for product in products:
        quantity = cart.get(str(product.id), 0)

        cart_total += product.price * quantity
        cart_count += quantity

    return {
        'cart_total': cart_total,
        'cart_count': cart_count,
    }