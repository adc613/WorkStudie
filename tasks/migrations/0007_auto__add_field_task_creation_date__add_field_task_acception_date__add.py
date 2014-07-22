# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Task.creation_date'
        db.add_column(u'tasks_task', 'creation_date',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Task.acception_date'
        db.add_column(u'tasks_task', 'acception_date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)

        # Adding field 'Task.completion_Date'
        db.add_column(u'tasks_task', 'completion_Date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Task.creation_date'
        db.delete_column(u'tasks_task', 'creation_date')

        # Deleting field 'Task.acception_date'
        db.delete_column(u'tasks_task', 'acception_date')

        # Deleting field 'Task.completion_Date'
        db.delete_column(u'tasks_task', 'completion_Date')


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
        u'tasks.bid': {
            'Meta': {'object_name': 'Bid'},
            'bid': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'bidder': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'max_length': '140', 'blank': 'True'})
        },
        u'tasks.review': {
            'Meta': {'object_name': 'Review'},
            'comments': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'review_creator'", 'null': 'True', 'to': u"orm['users.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rating': ('tasks.models.IntegerRangeField', [], {'name': "'rating'"})
        },
        u'tasks.task': {
            'Meta': {'object_name': 'Task'},
            'accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'accepted_bid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'accepted_bid'", 'null': 'True', 'to': u"orm['tasks.Bid']"}),
            'acception_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'bids': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['tasks.Bid']", 'null': 'True', 'blank': 'True'}),
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'completion_Date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'task_creator'", 'to': u"orm['users.User']"}),
            'creator_review': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'task_create_review'", 'null': 'True', 'to': u"orm['tasks.Review']"}),
            'discription': ('django.db.models.fields.TextField', [], {'max_length': '420'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'suggested_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'worker': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'task_worker'", 'null': 'True', 'to': u"orm['users.User']"}),
            'worker_review': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'task_worker_review'", 'null': 'True', 'to': u"orm['tasks.Review']"})
        },
        u'users.profile': {
            'Meta': {'object_name': 'Profile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'skills_discription': ('django.db.models.fields.TextField', [], {'max_length': "'1000'", 'blank': 'True'}),
            'tasks_completed': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'tasks_completed'", 'symmetrical': 'False', 'to': u"orm['tasks.Task']"}),
            'tasks_made': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'task_made'", 'symmetrical': 'False', 'to': u"orm['tasks.Task']"})
        },
        u'users.user': {
            'Meta': {'object_name': 'User'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '100', 'primary_key': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_worker': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_profile'", 'null': 'True', 'to': u"orm['users.Profile']"}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"})
        }
    }

    complete_apps = ['tasks']