from itertools import chain
from operator import attrgetter
from django.views.generic.base import TemplateView
from structure.models import Issue
from stories.models import Story
from blog.models import Entry
from video.models import Video
from config.models import SiteConfig


class CurrentView(TemplateView):
    def get_context_data(self, **kwargs):
        context = {}
        context['sections'] = Issue.objects.latest().sections.get_sections()
        return context


class FrontView(CurrentView):
    '''
    Front Page
    '''
    template_name = 'front.html'

    def get_context_data(self, **kwargs):
        context = super(FrontView, self).get_context_data(**kwargs)

        latest_stories = Story.published.order_by('-pub_date')[:10]
        latest_entries = Entry.objects.filter(is_published=True) \
            .order_by('-pub_date')[:10]
        latest_video = Video.published.latest('pub_date')
        context['latest_stories'] = sorted(chain( \
            latest_stories, latest_entries), key=attrgetter('pub_date'))[:5]

        latest_section = []
        for section in context['sections']:
            latest_section.extend(Story.published.filter(
                section=section, featured=True, \
                storyphoto__isnull=False).order_by('-pub_date')[:1])

        config = SiteConfig.get()
        context['featured'] = config.featuredstory_set.all() \
            .order_by('story_order')
        context['latest_entries'] = latest_entries
        context['latest_section'] = latest_section
        context['latest_video'] = latest_video
        return context
