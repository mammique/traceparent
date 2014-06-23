# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Scope'
        db.create_table(u'tp_monitor_scope', (
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='scopes_created', to=orm['tp_auth.User'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='scopes', to=orm['tp_auth.User'])),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'tp_monitor', ['Scope'])

        # Adding M2M table for field quantities on 'Scope'
        db.create_table(u'tp_monitor_scope_quantities', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('scope', models.ForeignKey(orm[u'tp_monitor.scope'], null=False)),
            ('quantity', models.ForeignKey(orm[u'tp_value.quantity'], null=False))
        ))
        db.create_unique(u'tp_monitor_scope_quantities', ['scope_id', 'quantity_id'])

        # Adding model 'Counter'
        db.create_table(u'tp_monitor_counter', (
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='counters_created', to=orm['tp_auth.User'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='counters', to=orm['tp_auth.User'])),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('datetime_start', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('datetime_stop', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal(u'tp_monitor', ['Counter'])

        # Adding M2M table for field scopes on 'Counter'
        db.create_table(u'tp_monitor_counter_scopes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('counter', models.ForeignKey(orm[u'tp_monitor.counter'], null=False)),
            ('scope', models.ForeignKey(orm[u'tp_monitor.scope'], null=False))
        ))
        db.create_unique(u'tp_monitor_counter_scopes', ['counter_id', 'scope_id'])

        # Adding M2M table for field quantities on 'Counter'
        db.create_table(u'tp_monitor_counter_quantities', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('counter', models.ForeignKey(orm[u'tp_monitor.counter'], null=False)),
            ('quantity', models.ForeignKey(orm[u'tp_value.quantity'], null=False))
        ))
        db.create_unique(u'tp_monitor_counter_quantities', ['counter_id', 'quantity_id'])

        # Adding model 'ResultSum'
        db.create_table(u'tp_monitor_resultsum', (
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('quantity', self.gf('django.db.models.fields.DecimalField')(max_digits=64, decimal_places=30)),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tp_value.Unit'])),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tp_value.QuantityStatus'])),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('counter', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sums', to=orm['tp_monitor.Counter'])),
        ))
        db.send_create_signal(u'tp_monitor', ['ResultSum'])

        # Adding model 'Mark'
        db.create_table(u'tp_monitor_mark', (
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('quantity', self.gf('traceparent.fields.DecimalBlankToNoneField')(null=True, max_digits=64, decimal_places=30, blank=True)),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tp_value.Unit'])),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='marks_created', to=orm['tp_auth.User'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='marks', to=orm['tp_auth.User'])),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'tp_monitor', ['Mark'])

        # Adding M2M table for field statuses on 'Mark'
        db.create_table(u'tp_monitor_mark_statuses', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mark', models.ForeignKey(orm[u'tp_monitor.mark'], null=False)),
            ('quantitystatus', models.ForeignKey(orm[u'tp_value.quantitystatus'], null=False))
        ))
        db.create_unique(u'tp_monitor_mark_statuses', ['mark_id', 'quantitystatus_id'])

        # Adding M2M table for field counters on 'Mark'
        db.create_table(u'tp_monitor_mark_counters', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mark', models.ForeignKey(orm[u'tp_monitor.mark'], null=False)),
            ('counter', models.ForeignKey(orm[u'tp_monitor.counter'], null=False))
        ))
        db.create_unique(u'tp_monitor_mark_counters', ['mark_id', 'counter_id'])


    def backwards(self, orm):
        # Deleting model 'Scope'
        db.delete_table(u'tp_monitor_scope')

        # Removing M2M table for field quantities on 'Scope'
        db.delete_table('tp_monitor_scope_quantities')

        # Deleting model 'Counter'
        db.delete_table(u'tp_monitor_counter')

        # Removing M2M table for field scopes on 'Counter'
        db.delete_table('tp_monitor_counter_scopes')

        # Removing M2M table for field quantities on 'Counter'
        db.delete_table('tp_monitor_counter_quantities')

        # Deleting model 'ResultSum'
        db.delete_table(u'tp_monitor_resultsum')

        # Deleting model 'Mark'
        db.delete_table(u'tp_monitor_mark')

        # Removing M2M table for field statuses on 'Mark'
        db.delete_table('tp_monitor_mark_statuses')

        # Removing M2M table for field counters on 'Mark'
        db.delete_table('tp_monitor_mark_counters')


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
        u'tp_monitor.counter': {
            'Meta': {'ordering': "['-datetime']", 'object_name': 'Counter'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'counters_created'", 'to': u"orm['tp_auth.User']"}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'datetime_start': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'datetime_stop': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'quantities': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'counters'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['tp_value.Quantity']"}),
            'scopes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'counters'", 'symmetrical': 'False', 'to': u"orm['tp_monitor.Scope']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'counters'", 'to': u"orm['tp_auth.User']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
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
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        u'tp_monitor.resultsum': {
            'Meta': {'ordering': "['-datetime']", 'object_name': 'ResultSum'},
            'counter': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sums'", 'to': u"orm['tp_monitor.Counter']"}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.DecimalField', [], {'max_digits': '64', 'decimal_places': '30'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tp_value.QuantityStatus']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tp_value.Unit']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        u'tp_monitor.scope': {
            'Meta': {'ordering': "['-datetime']", 'object_name': 'Scope'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scopes_created'", 'to': u"orm['tp_auth.User']"}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'quantities': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'scopes'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['tp_value.Quantity']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scopes'", 'to': u"orm['tp_auth.User']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
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
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
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
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        }
    }

    complete_apps = ['tp_monitor']