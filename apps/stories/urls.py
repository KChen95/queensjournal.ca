from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^(?P<datestring>\d{4}-\d{1,2}-\d{1,2})/$',
        'archive.views.archive_issue_index', name='archive-issue-index'),

    url(r'^(?P<datestring>\d{4}-\d{1,2}-\d{1,2})/(?P<section>[-\w]+)/$',
        'archive.views.section_index', name='archive-section-index'),

    url(r'^(?P<datestring>\d{4}-\d{1,2}-\d{1,2})/(?P<section>[-\w]+)/(?P<slug>[-\w]+)/$',
        'stories.views.detail_story', name='story-detail'),

    (r'^(?P<datestring>\d{4}-\d{1,2}-\d{1,2})/(?P<section>[-\w]+)/(?P<slug>[-\w]+)/email/$',
        'stories.views.email_story'),

    (r'^(?P<section>[-\w]+)/$', 'stories.views.index_section'),
)
