from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from django.views.decorators.http import require_POST


def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get('cart', {})

    product_id = str(product.id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart

    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = request.session.get('cart', {})

    products = Product.objects.filter(id__in=cart.keys())

    total_price = 0

    for product in products:
        
        product.quantity = cart[str(product.id)]
        product.subtotal = product.price * product.quantity
        total_price += product.subtotal

    context = {
        'products': products,
        'cart': cart,
        'total_price': total_price,
    }

    return render(request, 'cart/cart_detail.html', context)

def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart

    return redirect('cart:cart_detail')


@require_POST
def cart_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get('cart', {})
    product_id = str(product.id)

    quantity = int(request.POST.get('quantity', 1))

    if quantity <= 0:
        cart.pop(product_id, None)
    else:
        cart[product_id] = quantity

    request.session['cart'] = cart

    return redirect('cart:cart_detail')
