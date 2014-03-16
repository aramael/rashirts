# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Order.email'
        db.add_column(u'shop_order', 'email',
                      self.gf('django.db.models.fields.EmailField')(default='', max_length=75),
                      keep_default=False)

        # Adding field 'Order.stripe_customer'
        db.add_column(u'shop_order', 'stripe_customer',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Order.purchase_time'
        db.add_column(u'shop_order', 'purchase_time',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)

        # Adding field 'Order.amount_due'
        db.add_column(u'shop_order', 'amount_due',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=2),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Order.email'
        db.delete_column(u'shop_order', 'email')

        # Deleting field 'Order.stripe_customer'
        db.delete_column(u'shop_order', 'stripe_customer')

        # Deleting field 'Order.purchase_time'
        db.delete_column(u'shop_order', 'purchase_time')

        # Deleting field 'Order.amount_due'
        db.delete_column(u'shop_order', 'amount_due')


    models = {
        u'shop.order': {
            'Meta': {'object_name': 'Order'},
            'address_city': ('django.db.models.fields.TextField', [], {}),
            'address_country': ('django.db.models.fields.TextField', [], {}),
            'address_line_1': ('django.db.models.fields.TextField', [], {}),
            'address_line_2': ('django.db.models.fields.TextField', [], {}),
            'address_state': ('django.db.models.fields.TextField', [], {}),
            'address_zip': ('django.db.models.fields.TextField', [], {}),
            'amount_due': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'}),
            'email': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.TextField', [], {}),
            'purchase_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'stripe_customer': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'stripe_token': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['shop']