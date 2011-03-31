from django.conf.urls.defaults import *
from feeds import *

feeds = {
    'latest': LatestStories,
    'section': LatestStoriesSection,
    'allblogs': LatestPostsAllBlogs,
    'blogs': LatestPostsSingleBlog,
    'blog-author': LatestPostsSingleAuthor,
##    'calendar': LatestCalendar,
}

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
	
urlpatterns = patterns('',
	(r'^polls/', include('polls.urls')),
	(r'^comments/', include('django.contrib.comments.urls')),
	(r'^story/', include('stories.urls')),
	(r'^$', 'stories.views.index_front'),
	(r'^blogs/', include('blog.urls')),
	(r'^staff/', include('staff.urls')),
	(r'^search/', include('haystack.urls')),
	(r'^rss/(?P<url>.*)/', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
	
	# Uncomment the admin/doc line below to enable admin documentation:
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	(r'^admin/', include(admin.site.urls)),
	
	(r'^tags/$', 'stories.views.tags'),
	(r'^tag/(?P<tag>[a-zA-Z0-9_.-]+)/$','stories.views.with_tag'),
	(r'^tag/(?P<tag>[a-zA-Z0-9_.-]+)/page/(?P<id>[-\w]+)/$', 'stories.views.with_tag' ),
	
	('^s/', include('shorturls.urls')),
	
	#(r'^grappelli/', include('grappelli.urls')),
	
	
	# Because I have the URL regexing words as sections, this pattern needs to be last.
	# If you put anything after, the CONF will think it's a section and you won't get anywhere.
	## THE FOLLOWING LINE MUST BE THE LAST URL IN THE CONF
	(r'^(?P<section>[-\w]+)/', 'stories.views.index_section'),
	## DO NOT ADD ANY URLS AFTER THIS LINE
)