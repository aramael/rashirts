import stripe
import json

from django.conf import settings
from django.db import models

# Setup Stripe API
stripe.api_key = settings.STRIPE_PRIVATE_KEY


class Order(models.Model):

    SIZES = {
        'S': 'Small',
        'M': 'Medium',
        'L': 'Large',
        'XL': 'Extra Large',
        '2XL': 'Extra Extra Large',
    }

    SHIRTS = {
        'W': 'Women\'s Tank',
        'L': 'Lacrosse Tank'
    }

    name = models.CharField(blank=False, null=False, max_length=100)
    email = models.EmailField(blank=True, default='')
    address_line_1 = models.TextField()
    address_line_2 = models.TextField(blank=True, default='')
    address_city = models.TextField()
    address_state = models.TextField()
    address_zip = models.TextField()
    address_country = models.TextField()

    stripe_token = models.CharField(blank=False, null=False, max_length=100)
    stripe_customer = models.CharField(max_length=50, blank=True, null=True)
    purchase_time = models.DateTimeField(null=True, blank=True)
    amount_due = models.DecimalField(decimal_places=2, max_digits=8, default=0, blank=True)

    order = models.TextField(blank=False, null=False)

    def order_pretty(self):

        order = u""

        for item in json.loads(self.order):

            item['size'] = self.SIZES[item['size']]
            item['type'] = self.SHIRTS.get(item['type'], 'Discontinued')

            order += u"{quantity} <strong>{size}</strong> {type} <br/>".format(**item)

        return order
    order_pretty.allow_tags = True
    order_pretty.short_description = 'Order'

    def shirt_count(self):

        count = 0

        for item in json.loads(self.order):
            count += int(item['quantity'])

        return count
    order_pretty.short_description = 'Shirt Count'

    def refund_charge(self):

        # Capture the Pre-Authorised Card
        ch = stripe.Charge.retrieve(self.stripe_token)
        ch.refund()
        self.save()