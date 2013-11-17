# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Range.latitude'
        db.add_column(u'geoip_range', 'latitude',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=6, blank=True),
                      keep_default=False)

        # Adding field 'Range.longitude'
        db.add_column(u'geoip_range', 'longitude',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=6, blank=True),
                      keep_default=False)

        # Deleting field 'City.longitude'
        db.delete_column(u'geoip_city', 'longitude')

        # Deleting field 'City.latitude'
        db.delete_column(u'geoip_city', 'latitude')


    def backwards(self, orm):
        # Deleting field 'Range.latitude'
        db.delete_column(u'geoip_range', 'latitude')

        # Deleting field 'Range.longitude'
        db.delete_column(u'geoip_range', 'longitude')

        # Adding field 'City.longitude'
        db.add_column(u'geoip_city', 'longitude',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=6, blank=True),
                      keep_default=False)

        # Adding field 'City.latitude'
        db.add_column(u'geoip_city', 'latitude',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=6, blank=True),
                      keep_default=False)


    models = {
        u'geoip.area': {
            'Meta': {'unique_together': "(('country', 'name'),)", 'object_name': 'Area'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geoip.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'geoip.city': {
            'Meta': {'unique_together': "(('area', 'name'),)", 'object_name': 'City'},
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geoip.Area']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'geoip.country': {
            'Meta': {'object_name': 'Country'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'geoip.isp': {
            'Meta': {'unique_together': "(('country', 'name'),)", 'object_name': 'ISP'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geoip.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'geoip.provider': {
            'Meta': {'object_name': 'Provider'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isp': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['geoip.ISP']", 'symmetrical': 'False', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'ranges': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'geoip.range': {
            'Meta': {'object_name': 'Range'},
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geoip.Area']", 'null': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geoip.City']", 'null': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geoip.Country']"}),
            'end_ip': ('django.db.models.fields.BigIntegerField', [], {'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isp': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geoip.ISP']", 'null': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '6', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '6', 'blank': 'True'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geoip.Provider']", 'null': 'True'}),
            'start_ip': ('django.db.models.fields.BigIntegerField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['geoip']