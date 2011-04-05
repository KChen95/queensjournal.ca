from datetime import datetime, timedelta
from django.contrib.syndication.views import Feed
from structure.models import Issue, Section, FlatPlanConfig
from stories.models import Story
from sidebars.models import NewsCalendarItem, ArtsCalendarItem, SportsCalendarItem
from blog.models import Blog, Entry
from structure.models import Author


class LatestStories(Feed):
	title = "Queen's Journal: Latest stories"
	link = "/"
	description = "All the latest stories from the Queen's Journal."
	description_template = 'feeds/stories_description.html'

	def items(self):
		return Story.objects.filter(status='p').order_by('-pub_date')[:10]

	def item_author_name(self, item):
		return item.list_authors()
			
	def item_pubdate(self, item):
		return item.pub_date

class LatestStoriesSection(Feed):
	def get_object(self, bits):
		"""
		/rss/section/<section>/: latest stories from <section>
		"""
		if len(bits) != 1:
			raise ObjectDoesNotExist
		else:
			return Section.objects.get(slug__exact=bits[0])
		
	def title(self, obj):
		return "Queen's Journal: Latest stories in %s" % obj.name

	def link(self, obj):
		return obj.get_absolute_url()

	def description(self, obj):
		return "The latest stories in %s from the Queen's Journal." % obj.name

	def items(self, obj):
		return Story.objects.select_related().filter(section__slug=obj.slug, issue__is_published='PUB').order_by('-structure_issue.pub_date','section','section_order')[:15]

	def item_author_name(self, item):
		return item.list_authors()

	def item_pubdate(self, item):
		return item.issue.pub_date


class LatestPostsAllBlogs(Feed):
	title = "Queen's Journal: Latest posts from all blogs"
	link = "/blogs/"
	description = "All the latest blog posts from the Queen's Journal."

	def items(self):
		return Entry.objects.select_related().filter(is_published=True).order_by('-date_published')[:15]

	def item_author_name(self, item):
		return item.author.user.get_full_name()

	def item_pubdate(self, item):
		return item.date_published


class LatestPostsSingleBlog(Feed):
	def get_object(self, bits):
		"""
		/rss/blogs/<blog>/: latest posts from <blog>
		"""
		if len(bits) != 1:
			raise ObjectDoesNotExist
		else:
			return Blog.objects.get(slug__exact=bits[0])
		
	def title(self, obj):
		return "Queen's Journal: Latest blog posts in %s" % obj.title

	def link(self, obj):
		return obj.get_absolute_url()

	def description(self, obj):
		return "The latest blog posts in %s from the Queen's Journal." % obj.title

	def items(self, obj):
		return Entry.objects.select_related().filter(blog__slug=obj.slug, is_published=True).order_by('-date_published')[:15]

	def item_author_name(self, item):
		return item.author.user.get_full_name()

	def item_pubdate(self, item):
		return item.date_published


class LatestPostsSingleAuthor(Feed):
	def get_object(self, bits):
		"""
		/rss/author/<author-id>/: latest posts from <author-id>
		"""
		if len(bits) != 1:
			raise ObjectDoesNotExist
		else:
			return Author.objects.get(pk=bits[0])
		
	def title(self, obj):
		return "Queen's Journal: Latest blog posts from %s" % obj.user.get_full_name()

	def link(self, obj):
		return obj.get_absolute_url()

	def description(self, obj):
		return "The latest blog posts by %s from the Queen's Journal." % obj.user.get_full_name()

	def items(self, obj):
		return Entry.objects.select_related().filter(author=obj, is_published=True).order_by('-date_published')[:15]

	def item_author_name(self, item):
		return item.author.user.get_full_name()

	def item_pubdate(self, item):
		return item.date_published

