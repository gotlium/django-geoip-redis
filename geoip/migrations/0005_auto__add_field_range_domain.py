# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Range.domain'
        db.add_column(u'geoip_range', 'domain',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geoip.Domain'], null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Range.domain'
        db.delete_column(u'geoip_range', 'domain_id')


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
        u'geoip.domain': {
            'Meta': {'object_name': 'Domain'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'geoip.isp': {
            'Meta': {'unique_together': "(('country', 'name'),)", 'object_name': 'ISP'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geoip.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '75'})
        },
        u'geoip.netspeed': {
            'Meta': {'object_name': 'NetSpeed'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'})
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
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geoip.Domain']", 'null': 'True'}),
            'end_ip': ('django.db.models.fields.BigIntegerField', [], {'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isp': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geoip.ISP']", 'null': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '6', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '6', 'blank': 'True'}),
            'metro_code': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geoip.Provider']", 'null': 'True'}),
            'speed': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geoip.NetSpeed']", 'null': 'True'}),
            'start_ip': ('django.db.models.fields.BigIntegerField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['geoip']