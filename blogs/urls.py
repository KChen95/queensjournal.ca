from django.conf.urls.defaults import *
from journal.blogs.views import *

urlpatterns = patterns('',
    url(r'^archived/$', all_blogs, {'active': False}, name='all_blogs_archived'),
    url(r'^(?P<blog>[-\w]+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[-\w]+)/$', blog_detail),
    url(r'^(?P<blog>[-\w]+)/(?P<year>\d{4})/(?P<month>\d{2})/page/(?P<page>\d{1,5})/$', blog_archive_month, name='blog_archive_month_pages'),
    url(r'^(?P<blog>[-\w]+)/(?P<year>\d{4})/(?P<month>\d{2})/$', blog_archive_month, name='blog_archive_month_front'),
    url(r'^(?P<blog>[-\w]+)/author/(?P<author_id>\d{1,5})/page/(?P<page>\d{1,5})/$', blog_archive_author, name='blog_archive_author_pages'),
    url(r'^(?P<blog>[-\w]+)/author/(?P<author_id>\d{1,5})/$', blog_archive_author, name='blog_archive_author_front'),
    url(r'^(?P<blog>[-\w]+)/category/(?P<cat_slug>[-\w]+)/page/(?P<page>\d{1,5})/$', blog_archive_category, name='blog_archive_category_pages'),
    url(r'^(?P<blog>[-\w]+)/category/(?P<cat_slug>[-\w]+)/$', blog_archive_category, name='blog_archive_category_front'),
    url(r'^(?P<blog>[-\w]+)/search/$', blog_search, name='blog_search'),            
    url(r'^(?P<blog>[-\w]+)/page/(?P<page>\d{1,5})/$', blog_index, name='blog_index_pages'),
    url(r'^profile/(?P<author_id>\d{1,5})/', blog_author, name='blog_author'),
    url(r'^(?P<blog>[-\w]+)/bloggers/', blog_all_authors, name='blog_all_authors'),
    url(r'^(?P<blog>[-\w]+)/$', blog_index, name='blog_index_front'),
    url(r'^$', all_blogs, name='all_blogs'),
    )
