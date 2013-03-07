# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Unit'
        db.create_table(u'tp_value_unit', (
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tp_auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=128)),
            ('symbol', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('decimal_places', self.gf('django.db.models.fields.PositiveIntegerField')(default=2, null=True, blank=True)),
        ))
        db.send_create_signal(u'tp_value', ['Unit'])

        # Adding model 'Quantity'
        db.create_table(u'tp_value_quantity', (
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='quantities_created', null=True, to=orm['tp_auth.User'])),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tp_value.Unit'])),
            ('quantity', self.gf('django.db.models.fields.DecimalField')(max_digits=64, decimal_places=30)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='quantities', null=True, to=orm['tp_auth.User'])),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('status', self.gf('django.db.models.fields.SlugField')(default='symbolic', max_length=64)),
        ))
        db.send_create_signal(u'tp_value', ['Quantity'])

        # Adding M2M table for field previous on 'Quantity'
        db.create_table(u'tp_value_quantity_previous', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_quantity', models.ForeignKey(orm[u'tp_value.quantity'], null=False)),
            ('to_quantity', models.ForeignKey(orm[u'tp_value.quantity'], null=False))
        ))
        db.create_unique(u'tp_value_quantity_previous', ['from_quantity_id', 'to_quantity_id'])


    def backwards(self, orm):
        # Deleting model 'Unit'
        db.delete_table(u'tp_value_unit')

        # Deleting model 'Quantity'
        db.delete_table(u'tp_value_quantity')

        # Removing M2M table for field previous on 'Quantity'
        db.delete_table('tp_value_quantity_previous')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'tp_auth.user': {
            'Meta': {'object_name': 'User'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tp_auth.User']", 'null': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        u'tp_value.quantity': {
            'Meta': {'ordering': "['-datetime']", 'object_name': 'Quantity'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'quantities_created'", 'null': 'True', 'to': u"orm['tp_auth.User']"}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'previous': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'next'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['tp_value.Quantity']"}),
            'quantity': ('django.db.models.fields.DecimalField', [], {'max_digits': '64', 'decimal_places': '30'}),
            'status': ('django.db.models.fields.SlugField', [], {'default': "'symbolic'", 'max_length': '64'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tp_value.Unit']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'quantities'", 'null': 'True', 'to': u"orm['tp_auth.User']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        u'tp_value.unit': {
            'Meta': {'object_name': 'Unit'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tp_auth.User']"}),
            'decimal_places': ('django.db.models.fields.PositiveIntegerField', [], {'default': '2', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '128'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        }
    }

    complete_apps = ['tp_value']