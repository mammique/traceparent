# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Snippet'
        db.create_table(u'tp_metadata_snippet', (
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='metadata_snippets_created', to=orm['tp_auth.User'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='metadata_snippets', to=orm['tp_auth.User'])),
            ('visibility', self.gf('django.db.models.fields.SlugField')(default='public', max_length=64)),
            ('mimetype', self.gf('django.db.models.fields.SlugField')(default='text/plain', max_length=64)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=128)),
            ('type', self.gf('traceparent.fields.SlugBlankToNoneField')(default=None, max_length=64, null=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'tp_metadata', ['Snippet'])

        # Adding M2M table for field assigned_users on 'Snippet'
        db.create_table(u'tp_metadata_snippet_assigned_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('snippet', models.ForeignKey(orm[u'tp_metadata.snippet'], null=False)),
            ('user', models.ForeignKey(orm[u'tp_auth.user'], null=False))
        ))
        db.create_unique(u'tp_metadata_snippet_assigned_users', ['snippet_id', 'user_id'])

        # Adding M2M table for field assigned_units on 'Snippet'
        db.create_table(u'tp_metadata_snippet_assigned_units', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('snippet', models.ForeignKey(orm[u'tp_metadata.snippet'], null=False)),
            ('unit', models.ForeignKey(orm[u'tp_value.unit'], null=False))
        ))
        db.create_unique(u'tp_metadata_snippet_assigned_units', ['snippet_id', 'unit_id'])

        # Adding M2M table for field assigned_quantities on 'Snippet'
        db.create_table(u'tp_metadata_snippet_assigned_quantities', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('snippet', models.ForeignKey(orm[u'tp_metadata.snippet'], null=False)),
            ('quantity', models.ForeignKey(orm[u'tp_value.quantity'], null=False))
        ))
        db.create_unique(u'tp_metadata_snippet_assigned_quantities', ['snippet_id', 'quantity_id'])


    def backwards(self, orm):
        # Deleting model 'Snippet'
        db.delete_table(u'tp_metadata_snippet')

        # Removing M2M table for field assigned_users on 'Snippet'
        db.delete_table('tp_metadata_snippet_assigned_users')

        # Removing M2M table for field assigned_units on 'Snippet'
        db.delete_table('tp_metadata_snippet_assigned_units')

        # Removing M2M table for field assigned_quantities on 'Snippet'
        db.delete_table('tp_metadata_snippet_assigned_quantities')


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
        u'tp_metadata.snippet': {
            'Meta': {'ordering': "['-slug', '-datetime']", 'object_name': 'Snippet'},
            'assigned_quantities': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'assigned_metadata_snippets'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['tp_value.Quantity']"}),
            'assigned_units': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'assigned_metadata_snippets'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['tp_value.Unit']"}),
            'assigned_users': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'assigned_metadata_snippets'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['tp_auth.User']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'metadata_snippets_created'", 'to': u"orm['tp_auth.User']"}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'mimetype': ('django.db.models.fields.SlugField', [], {'default': "'text/plain'", 'max_length': '64'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '128'}),
            'type': ('traceparent.fields.SlugBlankToNoneField', [], {'default': 'None', 'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'metadata_snippets'", 'to': u"orm['tp_auth.User']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'visibility': ('django.db.models.fields.SlugField', [], {'default': "'public'", 'max_length': '64'})
        },
        u'tp_value.quantity': {
            'Meta': {'ordering': "['-datetime']", 'object_name': 'Quantity'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'quantities_created'", 'to': u"orm['tp_auth.User']"}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'prev': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'next'", 'null': 'True', 'to': u"orm['tp_value.Quantity']"}),
            'quantity': ('django.db.models.fields.DecimalField', [], {'max_digits': '64', 'decimal_places': '30'}),
            'status': ('traceparent.fields.SlugBlankToNoneField', [], {'default': 'None', 'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tp_value.Unit']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'quantities'", 'to': u"orm['tp_auth.User']"}),
            'user_visibility': ('django.db.models.fields.SlugField', [], {'default': "'public'", 'max_length': '64'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        u'tp_value.unit': {
            'Meta': {'ordering': "['-name']", 'object_name': 'Unit'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'units_created'", 'to': u"orm['tp_auth.User']"}),
            'decimal_places': ('django.db.models.fields.PositiveIntegerField', [], {'default': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '128'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        }
    }

    complete_apps = ['tp_metadata']