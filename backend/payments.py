import stripe
from flask import jsonify

stripe.api_key = "YOUR_STRIPE_SECRET_KEY"

def create_checkout():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': 'Pro Resume Plan'},
                'unit_amount': 500,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='https://your-site.com/success',
        cancel_url='https://your-site.com/cancel',
    )

    return jsonify({'url': session.url})
