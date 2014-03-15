import stripe
import json

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template import loader

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

    def mail_customer(self, subject, body):
        msg = EmailMultiAlternatives(subject, '', None, [self.email, ])
        msg.attach_alternative(body, "text/html")
        msg.track_opens = True
        msg.track_clicks = True
        msg.auto_text = True
        msg.send()

    def receipt_email_message(self, subject_template='email/receipt_delivery_subject.txt',
                              email_template='email/receipt_delivery.html', extra_context=None):

        ch = stripe.Charge.retrieve(self.stripe_token)

        context = {
            'email': self.email,
            'name': self.name,
            'date': self.purchase_time,
            'price': ch.amount/100.00,
            'order_pretty': self.order_pretty(),
        }

        if extra_context is not None:
            context.update(extra_context)

        subject = loader.render_to_string(subject_template, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())

        context.update({'subject': subject})

        email = loader.render_to_string(email_template, context)

        return subject, email

    def send_receipt(self, *args, **kwargs):
        """
        Send out an email customer with a receipt for the purchase.
        """

        subject, email = self.receipt_email_message(*args, **kwargs)
        self.mail_customer(subject, email)

    def pickup_email_message(self, subject_template='email/item_pickup_subject.txt',
                             email_template='email/item_pickup.html', extra_context=None):

        #ch = stripe.Charge.retrieve(self.stripe_token)

        context = {
            'email': self.email,
            'name': self.name,
            'date': self.purchase_time,
            #'price': ch.amount/100.00,
            'order_pretty': self.order_pretty(),
        }

        if extra_context is not None:
            context.update(extra_context)

        subject = loader.render_to_string(subject_template, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())

        context.update({'subject': subject})

        email = loader.render_to_string(email_template, context)

        return subject, email

    def send_pickup(self, *args, **kwargs):
        """
        Send out an email customer with a receipt for the purchase.
        """

        subject, email = self.pickup_email_message(*args, **kwargs)
        self.mail_customer(subject, email)