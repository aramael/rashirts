import stripe
import logging
import json

from .models import Order
from django import forms
from django.conf import settings
from django.db import transaction


# Get an instance of a logger
logger = logging.getLogger(__name__)

# Setup Stripe API
stripe.api_key = settings.STRIPE_PRIVATE_KEY


class OrderForm(forms.ModelForm):

    CREDIT_CARD_ERRORS = {
        'incorrect_number': '',
        'invalid_number': 'It seems that you have mistyped your credit card number. Can you try typing it again?',
        'invalid_expiry_month': 'We think you\'ve mistyped the expiration month. Try copying it again.',
        'invalid_expiry_year': 'You may have mistyped the expiration year, maybe try copying it again.',
        'invalid_cvc': 'The CVC code, the three-digit card security code printed on the back signature panel of '
                       'the card or the four-digit code printed on the front side of the card above the number if '
                       'you have American Express, seems to be invalid. Please try typing it again.',
        'expired_card': 'The card that you entered is expired. Please try using a different card.',
        'incorrect_cvc': 'The CVC code, the three-digit card security code printed on the back signature panel of '
                         'the card or the four-digit code printed on the front side of the card above the number if '
                         'you have American Express, seems to be incorrect. Please try typing it again.',
        'incorrect_zip': 'You have provided the wrong ZIP code for the credit card. Remember this ZIP code is '
                         'not the ZIP code of where you currently live or reside; however, it is the ZIP code that '
                         'the credit card is registered under with your bank. Try typing it again.',
        'card_declined': 'The you supplied was declined. Try submitting it again, if it doesn\'t work again then try '
                         'calling your bank to see if there is an issue you need to resolve. You\'re bank\'s number '
                         'is on the back of you\'re card.',
        'processing_error': 'An error occurred while trying to process your card. Please try submitting again.',
    }

    class Meta:
        model = Order

    def clean(self):
        """
        The clean method will authorise a charge but not charge it in case
        another error is thrown. If it fails, it simply raises the error
        given from Stripe's library as a standard ValidationError for proper
         feedback however it is converted into a more friendly message by
         the ``CREDIT_CARD_ERRORS`` dictionary.
        """

        data = super(OrderForm, self).clean()

        token = stripe.Token.retrieve(data['stripe_token'])

        data['email'] = token.email

        shirts = 0
        for item in json.loads(data['order']):
            shirts += int(item['quantity'])

        data['amount_due'] = shirts * settings.SHIRT_PRICE*100

        try:
            # Credit Card Processing
            customer = stripe.Customer.create(description=data['name'],
                                              email=data['email'], card=token)

            data['stripe_customer'] = customer.id

            # Authorize the Charge but DO NOT CHARGE in case there is an error
            charge = stripe.Charge.create(description=data['name'] + ' <' + data['email'] + ' > - Shop RA Shirt Order',
                                          amount=data['amount_due'], currency='usd',
                                          capture=False, customer=customer.id)

            data['stripe_token'] = charge.id

        except stripe.CardError, e:
            # Since it's a decline, stripe.CardError will be caught
            body = e.json_body
            err = body['error']

            if err['type'] == 'card_error':

                error = [self.CREDIT_CARD_ERRORS.get(err['code'], self.CREDIT_CARD_ERRORS['processing_error'])]
                self._errors["stripe_token"] = self.error_class(error)
        except stripe.AuthenticationError, e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            logger.critical('Stripe Authentication Failed. ' + str(e.json_body))

        return data

    def save(self, *args, **kwargs):

        with transaction.atomic():
            # This code executes inside a transaction.
            ch = stripe.Charge.retrieve(self.instance.stripe_token)
            ch.capture()

            self.instance.amount_due -= ch.amount

            super(OrderForm,self).save(*args, **kwargs)