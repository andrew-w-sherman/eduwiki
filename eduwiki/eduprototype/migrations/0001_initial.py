# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table(u'eduprototype_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'eduprototype', ['User'])

        # Adding model 'WikiPage'
        db.create_table(u'eduprototype_wikipage', (
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True)),
            ('page_id', self.gf('django.db.models.fields.IntegerField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('mod_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('wikitext', self.gf('django.db.models.fields.CharField')(max_length=10000)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('disambiguation', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'eduprototype', ['WikiPage'])

        # Adding model 'Link'
        db.create_table(u'eduprototype_link', (
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(related_name='source', to=orm['eduprototype.WikiPage'])),
            ('target', self.gf('django.db.models.fields.related.ForeignKey')(related_name='target', to=orm['eduprototype.WikiPage'])),
            ('position', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
        ))
        db.send_create_signal(u'eduprototype', ['Link'])

        # Adding model 'Review'
        db.create_table(u'eduprototype_review', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('root', self.gf('django.db.models.fields.related.ForeignKey')(related_name='descendents', to=orm['eduprototype.WikiPage'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='children', to=orm['eduprototype.Review'])),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(related_name='reviews', to=orm['eduprototype.WikiPage'])),
            ('suggested_prereq_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('suggested_prereq', self.gf('django.db.models.fields.related.ForeignKey')(related_name='suggested_parents', to=orm['eduprototype.WikiPage'])),
        ))
        db.send_create_signal(u'eduprototype', ['Review'])

        # Adding M2M table for field presented_prereqs on 'Review'
        m2m_table_name = db.shorten_name(u'eduprototype_review_presented_prereqs')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('review', models.ForeignKey(orm[u'eduprototype.review'], null=False)),
            ('wikipage', models.ForeignKey(orm[u'eduprototype.wikipage'], null=False))
        ))
        db.create_unique(m2m_table_name, ['review_id', 'wikipage_id'])

        # Adding M2M table for field chosen_prereqs on 'Review'
        m2m_table_name = db.shorten_name(u'eduprototype_review_chosen_prereqs')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('review', models.ForeignKey(orm[u'eduprototype.review'], null=False)),
            ('wikipage', models.ForeignKey(orm[u'eduprototype.wikipage'], null=False))
        ))
        db.create_unique(m2m_table_name, ['review_id', 'wikipage_id'])

        # Adding model 'PrereqFeedback'
        db.create_table(u'eduprototype_prereqfeedback', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('prereq_page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eduprototype.WikiPage'])),
            ('was_good', self.gf('django.db.models.fields.BooleanField')()),
            ('suggested_distractor_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('suggested_distractor_page', self.gf('django.db.models.fields.related.ForeignKey')(related_name='suggested_to_distract', to=orm['eduprototype.WikiPage'])),
            ('suggested_distractor_snippet', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal(u'eduprototype', ['PrereqFeedback'])

        # Adding model 'DistractorFeedback'
        db.create_table(u'eduprototype_distractorfeedback', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eduprototype.User'])),
            ('snippet', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('was_good', self.gf('django.db.models.fields.BooleanField')()),
            ('distractor_page', self.gf('django.db.models.fields.related.ForeignKey')(related_name='feedback_as_distractor', to=orm['eduprototype.WikiPage'])),
            ('distracted_page', self.gf('django.db.models.fields.related.ForeignKey')(related_name='feedback_of_distractors', to=orm['eduprototype.WikiPage'])),
            ('review', self.gf('django.db.models.fields.related.ForeignKey')(related_name='distractor', to=orm['eduprototype.Review'])),
        ))
        db.send_create_signal(u'eduprototype', ['DistractorFeedback'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table(u'eduprototype_user')

        # Deleting model 'WikiPage'
        db.delete_table(u'eduprototype_wikipage')

        # Deleting model 'Link'
        db.delete_table(u'eduprototype_link')

        # Deleting model 'Review'
        db.delete_table(u'eduprototype_review')

        # Removing M2M table for field presented_prereqs on 'Review'
        db.delete_table(db.shorten_name(u'eduprototype_review_presented_prereqs'))

        # Removing M2M table for field chosen_prereqs on 'Review'
        db.delete_table(db.shorten_name(u'eduprototype_review_chosen_prereqs'))

        # Deleting model 'PrereqFeedback'
        db.delete_table(u'eduprototype_prereqfeedback')

        # Deleting model 'DistractorFeedback'
        db.delete_table(u'eduprototype_distractorfeedback')


    models = {
        u'eduprototype.distractorfeedback': {
            'Meta': {'object_name': 'DistractorFeedback'},
            'distracted_page': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'feedback_of_distractors'", 'to': u"orm['eduprototype.WikiPage']"}),
            'distractor_page': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'feedback_as_distractor'", 'to': u"orm['eduprototype.WikiPage']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'review': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'distractor'", 'to': u"orm['eduprototype.Review']"}),
            'snippet': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['eduprototype.User']"}),
            'was_good': ('django.db.models.fields.BooleanField', [], {})
        },
        u'eduprototype.link': {
            'Meta': {'object_name': 'Link'},
            'position': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'source'", 'to': u"orm['eduprototype.WikiPage']"}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'target'", 'to': u"orm['eduprototype.WikiPage']"})
        },
        u'eduprototype.prereqfeedback': {
            'Meta': {'object_name': 'PrereqFeedback'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prereq_page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['eduprototype.WikiPage']"}),
            'suggested_distractor_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'suggested_distractor_page': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'suggested_to_distract'", 'to': u"orm['eduprototype.WikiPage']"}),
            'suggested_distractor_snippet': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'was_good': ('django.db.models.fields.BooleanField', [], {})
        },
        u'eduprototype.review': {
            'Meta': {'object_name': 'Review'},
            'chosen_prereqs': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'sessions_chosen'", 'symmetrical': 'False', 'to': u"orm['eduprototype.WikiPage']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reviews'", 'to': u"orm['eduprototype.WikiPage']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children'", 'to': u"orm['eduprototype.Review']"}),
            'presented_prereqs': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'sessions_presented'", 'symmetrical': 'False', 'to': u"orm['eduprototype.WikiPage']"}),
            'root': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'descendents'", 'to': u"orm['eduprototype.WikiPage']"}),
            'suggested_prereq': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'suggested_parents'", 'to': u"orm['eduprototype.WikiPage']"}),
            'suggested_prereq_name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'eduprototype.user': {
            'Meta': {'object_name': 'User'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'eduprototype.wikipage': {
            'Meta': {'object_name': 'WikiPage'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'disambiguation': ('django.db.models.fields.BooleanField', [], {}),
            'links': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'backlinks'", 'symmetrical': 'False', 'through': u"orm['eduprototype.Link']", 'to': u"orm['eduprototype.WikiPage']"}),
            'mod_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'page_id': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'wikitext': ('django.db.models.fields.CharField', [], {'max_length': '10000'})
        }
    }

    complete_apps = ['eduprototype']