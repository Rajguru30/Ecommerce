from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from ecommerce.models import Product
from ecommerce import db
import razorpay

main = Blueprint('main', __name__)

# ✅ Razorpay Setup
RAZORPAY_KEY_ID = "rzp_test_vF1ZbSA33iyWxi"  # Replace with your Razorpay Key ID
RAZORPAY_SECRET = "VgcwERiivrJUtbZV8pWWBbyW"      # Replace with your Razorpay Secret
razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_SECRET))


# 🏠 Home Page (Featured Products)
@main.route('/')
def index():
    products = Product.query.limit(6).all()
    return render_template('index.html', products=products)


# 📦 Full Product Catalog
@main.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)


# 📄 About Page
@main.route('/about')
def about():
    return render_template('about.html')


# 🛒 View Cart
@main.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    cart_total = sum(item['price'] * item['quantity'] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, cart_total=cart_total)


# ➕ Add Product to Cart
@main.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    cart = session.get('cart', [])

    for item in cart:
        if item['id'] == product.id:
            item['quantity'] += 1
            break
    else:
        cart.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'quantity': 1
        })

    session['cart'] = cart
    flash(f"{product.name} added to cart.", "success")
    return redirect(url_for('main.cart'))


# ❌ Remove Product from Cart
@main.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != product_id]
    session['cart'] = cart
    flash("Item removed from cart.", "info")
    return redirect(url_for('main.cart'))


# 💳 Checkout with Razorpay
@main.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart_items = session.get('cart', [])
    if not cart_items:
        flash("Your cart is empty!", "warning")
        return redirect(url_for('main.cart'))

    cart_total = sum(item['price'] * item['quantity'] for item in cart_items)
    amount_paise = cart_total * 100  # Razorpay uses paise

    # Create Razorpay Order
    payment = razorpay_client.order.create({
        'amount': amount_paise,
        'currency': 'INR',
        'payment_capture': 1
    })

    return render_template('checkout.html',
                           cart_items=cart_items,
                           total=cart_total,
                           razorpay_order_id=payment['id'],
                           razorpay_key_id=RAZORPAY_KEY_ID)
