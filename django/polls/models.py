from datetime import datetime, timedelta
from django.db import models

class Poll(models.Model):
    question = models.CharField(max_length=255, unique=True)
    pub_date = models.DateTimeField('Publish date', default=datetime.now, help_text='The date when the poll goes live. Defaults to now.')
    close_date = models.DateTimeField(default=datetime.now()+timedelta(7), help_text='The date when the poll closes. Defaults to a week from now.')

    def total_votes(self):
        return Vote.objects.filter(poll=self.id).count()

    def is_active(self):
        return self.close_date > datetime.now()

    class Admin:
        list_display        = ('question','pub_date','close_date')

    class Meta:
        ordering            = ('-pub_date','question')
		
    def __unicode__(self):
        return u'%s' % self.question


class Choice(models.Model):
    choice = models.CharField(max_length=255)
    poll = models.ForeignKey(Poll)

    def votes(self):
        return self.vote_set.count()

    def __unicode__(self):
        return u'%s - %s' % (self.poll.question, self.choice)


class Vote(models.Model):
    choice = models.ForeignKey(Choice)
    poll = models.ForeignKey(Poll)
    ip_address = models.IPAddressField(blank=True, null=True, help_text='The originating IP address of the vote. May not represent the actual client IP (due to proxies, for example).')
    session_hash = models.CharField(max_length=32, help_text='The session hash sent with the vote.')
    submit_date = models.DateTimeField(default=datetime.now)

    class Admin:
        list_display        = ('ip_address','session_hash','submit_date','choice')
        list_filter         = ('poll','submit_date')
        search_fields       = ('ip_address',)

    def __unicode__(self):
        return u'%s on %s (%s)' % (self.ip_address, self.choice, self.submit_date.strftime('%m-%d-%Y, %H:%M:%S'))    
