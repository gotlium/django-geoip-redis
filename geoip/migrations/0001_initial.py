# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Country'
        db.create_table('geoip_country', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=2, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('geoip', ['Country'])

        # Adding model 'Area'
        db.create_table('geoip_area', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geoip.Country'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('geoip', ['Area'])

        # Adding unique constraint on 'Area', fields ['country', 'name']
        db.create_unique('geoip_area', ['country_id', 'name'])

        # Adding model 'City'
        db.create_table('geoip_city', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('area', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geoip.Area'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=6, blank=True)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=6, blank=True)),
        ))
        db.send_create_signal('geoip', ['City'])

        # Adding unique constraint on 'City', fields ['area', 'name']
        db.create_unique('geoip_city', ['area_id', 'name'])

        # Adding model 'ISP'
        db.create_table('geoip_isp', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geoip.Country'])),
        ))
        db.send_create_signal('geoip', ['ISP'])

        # Adding unique constraint on 'ISP', fields ['country', 'name']
        db.create_unique('geoip_isp', ['country_id', 'name'])

        # Adding model 'Provider'
        db.create_table('geoip_provider', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('ranges', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('geoip', ['Provider'])

        # Adding M2M table for field isp on 'Provider'
        db.create_table('geoip_provider_isp', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('provider', models.ForeignKey(orm['geoip.provider'], null=False)),
            ('isp', models.ForeignKey(orm['geoip.isp'], null=False))
        ))
        db.create_unique('geoip_provider_isp', ['provider_id', 'isp_id'])

        # Adding model 'Range'
        db.create_table('geoip_range', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_ip', self.gf('django.db.models.fields.BigIntegerField')(db_index=True)),
            ('end_ip', self.gf('django.db.models.fields.BigIntegerField')(db_index=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geoip.Country'])),
            ('area', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geoip.Area'], null=True)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geoip.City'], null=True)),
            ('isp', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geoip.ISP'], null=True)),
            ('provider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geoip.Provider'], null=True)),
        ))
        db.send_create_signal('geoip', ['Range'])


    def backwards(self, orm):
        # Removing unique constraint on 'ISP', fields ['country', 'name']
        db.delete_unique('geoip_isp', ['country_id', 'name'])

        # Removing unique constraint on 'City', fields ['area', 'name']
        db.delete_unique('geoip_city', ['area_id', 'name'])

        # Removing unique constraint on 'Area', fields ['country', 'name']
        db.delete_unique('geoip_area', ['country_id', 'name'])

        # Deleting model 'Country'
        db.delete_table('geoip_country')

        # Deleting model 'Area'
        db.delete_table('geoip_area')

        # Deleting model 'City'
        db.delete_table('geoip_city')

        # Deleting model 'ISP'
        db.delete_table('geoip_isp')

        # Deleting model 'Provider'
        db.delete_table('geoip_provider')

        # Removing M2M table for field isp on 'Provider'
        db.delete_table('geoip_provider_isp')

        # Deleting model 'Range'
        db.delete_table('geoip_range')


    models = {
        'geoip.area': {
            'Meta': {'unique_together': "(('country', 'name'),)", 'object_name': 'Area'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geoip.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'geoip.city': {
            'Meta': {'unique_together': "(('area', 'name'),)", 'object_name': 'City'},
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geoip.Area']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '6', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '6', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'geoip.country': {
            'Meta': {'object_name': 'Country'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'geoip.isp': {
            'Meta': {'unique_together': "(('country', 'name'),)", 'object_name': 'ISP'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geoip.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'geoip.provider': {
            'Meta': {'object_name': 'Provider'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isp': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['geoip.ISP']", 'symmetrical': 'False', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'ranges': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'geoip.range': {
            'Meta': {'object_name': 'Range'},
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geoip.Area']", 'null': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geoip.City']", 'null': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geoip.Country']"}),
            'end_ip': ('django.db.models.fields.BigIntegerField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isp': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geoip.ISP']", 'null': 'True'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geoip.Provider']", 'null': 'True'}),
            'start_ip': ('django.db.models.fields.BigIntegerField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['geoip']