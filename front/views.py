from django.views.generic.base import TemplateView

from issues.models import Issue
from stories.models import Story
from blog.models import Entry
from config.models import SiteConfig
from video.models import Video


class CurrentView(TemplateView):
    # TODO fuck this
    def get_context_data(self, **kwargs):
        context = super(CurrentView, self).get_context_data(**kwargs)
        context['sections'] = Issue.objects.latest().sections.get_sections()
        return context


class FrontView(CurrentView):
    '''
    Front Page
    '''
    template_name = 'front.html'

    def get_context_data(self, **kwargs):
        context = super(FrontView, self).get_context_data(**kwargs)

        # TODO fuck all of this too
        latest_entries = Entry.objects.filter(is_published=True) \
            .order_by('-pub_date')[:10]

        latest_section = []
        for section in context['sections']:
            latest_section.extend(Story.objects.published().filter(
                section=section, featured=True, \
                storyphoto__isnull=False).order_by('-pub_date')[:1])

        context['latest_entries'] = latest_entries
        context['latest_section'] = latest_section
        return context
