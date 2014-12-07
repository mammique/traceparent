# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ResultSum.mode'
        db.add_column(u'tp_monitor_resultsum', 'mode',
                      self.gf('django.db.models.fields.SlugField')(default='normal', max_length=64),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ResultSum.mode'
        db.delete_column(u'tp_monitor_resultsum', 'mode')


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
            'email_md5': ('django.db.models.fields.SlugField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '64', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True', 'db_index': 'True'})
        },
        u'tp_monitor.counter': {
            'Meta': {'ordering': "['-datetime']", 'object_name': 'Counter'},
            'converters': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'counters'", 'to': u"orm['tp_value.Converter']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True', 'db_index': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'counters_created'", 'to': u"orm['tp_auth.User']"}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'datetime_start': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'datetime_stop': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'quantities': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'counters'", 'to': u"orm['tp_value.Quantity']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True', 'db_index': 'True'}),
            'scopes': ('django.db.models.fields.related.ManyToManyField', [], {'db_index': 'True', 'related_name': "'counters'", 'symmetrical': 'False', 'to': u"orm['tp_monitor.Scope']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'counters'", 'to': u"orm['tp_auth.User']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True', 'db_index': 'True'})
        },
        u'tp_monitor.mark': {
            'Meta': {'ordering': "['-datetime']", 'object_name': 'Mark'},
            'counters': ('django.db.models.fields.related.ManyToManyField', [], {'db_index': 'True', 'related_name': "'marks'", 'symmetrical': 'False', 'to': u"orm['tp_monitor.Counter']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'marks_created'", 'to': u"orm['tp_auth.User']"}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'quantity': ('traceparent.fields.DecimalBlankToNoneField', [], {'db_index': 'True', 'null': 'True', 'max_digits': '64', 'decimal_places': '30', 'blank': 'True'}),
            'statuses': ('django.db.models.fields.related.ManyToManyField', [], {'db_index': 'True', 'related_name': "'marks'", 'symmetrical': 'False', 'to': u"orm['tp_value.QuantityStatus']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tp_value.Unit']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'marks'", 'to': u"orm['tp_auth.User']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True', 'db_index': 'True'})
        },
        u'tp_monitor.resultsum': {
            'Meta': {'ordering': "['-datetime']", 'object_name': 'ResultSum'},
            'counter': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sums'", 'to': u"orm['tp_monitor.Counter']"}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'mode': ('django.db.models.fields.SlugField', [], {'default': "'normal'", 'max_length': '64'}),
            'quantity': ('django.db.models.fields.DecimalField', [], {'max_digits': '64', 'decimal_places': '30'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tp_value.QuantityStatus']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tp_value.Unit']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True', 'db_index': 'True'})
        },
        u'tp_monitor.scope': {
            'Meta': {'ordering': "['-datetime']", 'object_name': 'Scope'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scopes_created'", 'to': u"orm['tp_auth.User']"}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'quantities': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'scopes'", 'to': u"orm['tp_value.Quantity']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scopes'", 'to': u"orm['tp_auth.User']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True', 'db_index': 'True'})
        },
        u'tp_value.converter': {
            'Meta': {'object_name': 'Converter'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'converters_created'", 'to': u"orm['tp_auth.User']"}),
            'script': ('django.db.models.fields.TextField', [], {}),
            'type': ('django.db.models.fields.SlugField', [], {'default': "'operation_basic'", 'max_length': '64'}),
            'unit_in': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'converters_in'", 'to': u"orm['tp_value.Unit']"}),
            'unit_out': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'converters_out'", 'to': u"orm['tp_value.Unit']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'converters'", 'to': u"orm['tp_auth.User']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True', 'db_index': 'True'})
        },
        u'tp_value.quantity': {
            'Meta': {'ordering': "['-datetime']", 'object_name': 'Quantity'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'quantities_created'", 'to': u"orm['tp_auth.User']"}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'prev': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'next'", 'null': 'True', 'db_index': 'True', 'to': u"orm['tp_value.Quantity']"}),
            'quantity': ('django.db.models.fields.DecimalField', [], {'max_digits': '64', 'decimal_places': '30', 'db_index': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'quantities'", 'to': u"orm['tp_value.QuantityStatus']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tp_value.Unit']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'quantities'", 'to': u"orm['tp_auth.User']"}),
            'user_visibility': ('django.db.models.fields.SlugField', [], {'default': "'public'", 'max_length': '64'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True', 'db_index': 'True'})
        },
        u'tp_value.quantitystatus': {
            'Meta': {'ordering': "['-slug']", 'object_name': 'QuantityStatus'},
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '64', 'primary_key': 'True'})
        },
        u'tp_value.unit': {
            'Meta': {'ordering': "['name']", 'object_name': 'Unit'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'units_created'", 'to': u"orm['tp_auth.User']"}),
            'decimal_places': ('django.db.models.fields.PositiveIntegerField', [], {'default': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '128'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '8', 'db_index': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True', 'db_index': 'True'})
        }
    }

    complete_apps = ['tp_monitor']