# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'Snippet', fields ['datetime']
        db.create_index(u'tp_metadata_snippet', ['datetime'])


    def backwards(self, orm):
        # Removing index on 'Snippet', fields ['datetime']
        db.delete_index(u'tp_metadata_snippet', ['datetime'])


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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        u'tp_metadata.snippet': {
            'Meta': {'ordering': "['-datetime']", 'object_name': 'Snippet'},
            'assigned_counters': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'assigned_metadata_snippets'", 'to': u"orm['tp_monitor.Counter']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True', 'db_index': 'True'}),
            'assigned_marks': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'assigned_metadata_snippets'", 'to': u"orm['tp_monitor.Mark']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True', 'db_index': 'True'}),
            'assigned_quantities': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'assigned_metadata_snippets'", 'to': u"orm['tp_value.Quantity']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True', 'db_index': 'True'}),
            'assigned_scopes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'assigned_metadata_snippets'", 'to': u"orm['tp_monitor.Scope']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True', 'db_index': 'True'}),
            'assigned_units': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'assigned_metadata_snippets'", 'to': u"orm['tp_value.Unit']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True', 'db_index': 'True'}),
            'assigned_users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'assigned_metadata_snippets'", 'to': u"orm['tp_auth.User']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True', 'db_index': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'metadata_snippets_created'", 'to': u"orm['tp_auth.User']"}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'mimetype': ('django.db.models.fields.SlugField', [], {'default': "'text/plain'", 'max_length': '64'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '128'}),
            'type': ('traceparent.fields.SlugBlankToNoneField', [], {'default': 'None', 'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'metadata_snippets'", 'to': u"orm['tp_auth.User']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True', 'db_index': 'True'}),
            'visibility': ('django.db.models.fields.SlugField', [], {'default': "'public'", 'max_length': '64'})
        },
        u'tp_monitor.counter': {
            'Meta': {'ordering': "['-datetime']", 'object_name': 'Counter'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'counters_created'", 'to': u"orm['tp_auth.User']"}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'datetime_start': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'datetime_stop': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'quantities': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'counters'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['tp_value.Quantity']"}),
            'scopes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'counters'", 'symmetrical': 'False', 'to': u"orm['tp_monitor.Scope']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'counters'", 'to': u"orm['tp_auth.User']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True', 'db_index': 'True'})
        },
        u'tp_monitor.mark': {
            'Meta': {'ordering': "['-datetime']", 'object_name': 'Mark'},
            'counters': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'marks'", 'symmetrical': 'False', 'to': u"orm['tp_monitor.Counter']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'marks_created'", 'to': u"orm['tp_auth.User']"}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'quantity': ('traceparent.fields.DecimalBlankToNoneField', [], {'null': 'True', 'max_digits': '64', 'decimal_places': '30', 'blank': 'True'}),
            'statuses': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'marks'", 'symmetrical': 'False', 'to': u"orm['tp_value.QuantityStatus']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tp_value.Unit']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'marks'", 'to': u"orm['tp_auth.User']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True', 'db_index': 'True'})
        },
        u'tp_monitor.scope': {
            'Meta': {'ordering': "['-datetime']", 'object_name': 'Scope'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scopes_created'", 'to': u"orm['tp_auth.User']"}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'quantities': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'scopes'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['tp_value.Quantity']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scopes'", 'to': u"orm['tp_auth.User']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True', 'db_index': 'True'})
        },
        u'tp_value.quantity': {
            'Meta': {'ordering': "['-datetime']", 'object_name': 'Quantity'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'quantities_created'", 'to': u"orm['tp_auth.User']"}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'prev': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'next'", 'null': 'True', 'to': u"orm['tp_value.Quantity']"}),
            'quantity': ('django.db.models.fields.DecimalField', [], {'max_digits': '64', 'decimal_places': '30'}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '128'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True', 'db_index': 'True'})
        }
    }

    complete_apps = ['tp_metadata']