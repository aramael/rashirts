# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Order'
        db.create_table(u'shop_order', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('stripe_token', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('address_line_1', self.gf('django.db.models.fields.TextField')()),
            ('address_line_2', self.gf('django.db.models.fields.TextField')()),
            ('address_city', self.gf('django.db.models.fields.TextField')()),
            ('address_state', self.gf('django.db.models.fields.TextField')()),
            ('address_zip', self.gf('django.db.models.fields.TextField')()),
            ('address_country', self.gf('django.db.models.fields.TextField')()),
            ('order', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'shop', ['Order'])


    def backwards(self, orm):
        # Deleting model 'Order'
        db.delete_table(u'shop_order')


    models = {
        u'shop.order': {
            'Meta': {'object_name': 'Order'},
            'address_city': ('django.db.models.fields.TextField', [], {}),
            'address_country': ('django.db.models.fields.TextField', [], {}),
            'address_line_1': ('django.db.models.fields.TextField', [], {}),
            'address_line_2': ('django.db.models.fields.TextField', [], {}),
            'address_state': ('django.db.models.fields.TextField', [], {}),
            'address_zip': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.TextField', [], {}),
            'stripe_token': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['shop']