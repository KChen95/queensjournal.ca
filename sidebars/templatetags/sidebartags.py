from datetime import datetime
from django import template
from stories.models import Story
from structure.models import Section, Issue
from sidebars.models import NewsCalendarItem, ArtsCalendarItem, TalkingHeadsItem, SportsCalendarItem
from sidebars.settings import *

register = template.Library()

class SidebarItemsByIssueNode(template.Node):
    """
    Returns sidebar items for a specific issue date.
    section: a Section object, determines type of sidebar items.
    num: Number of sidebar items to return.
    issue: an Issue object, determines date range of sidebar items.
    """
    def __init__(self, section, issue, num):
        self.section, self.num, self.issue = section, num, issue

    def render(self, context):
        # first, grab actual section/issue objects from context and
        # grab SidebarItem class and template file for section
        try:
            section_obj = template.resolve_variable(self.section, context)
            issue_obj = template.resolve_variable(self.issue, context)
            sidebar_args = SIDEBAR_SECTIONS[section_obj.slug]
            manager, template_file = sidebar_args[0], sidebar_args[1]
        except:
            # deals with situations where the sidebar slug doesn't exist in
            # the settings dictionary. Defaults to "Previous stories."
            manager, template_file = PreviousStories(Section.objects.filter(slug=section_obj.slug)[0], self.num), 'sidebars/previously_sidebar.html'
        # create template nodelist
        nodelist = template.loader.get_template(template_file).nodelist
        # create context for nodelist
        context.push()
        if Issue.objects.latest('pub_date') == issue_obj:
            context['items'] = manager.get_future()
        else:
            context['items'] = manager.get_by_issue(issue_obj)
        if len(list(context['items'])) == 0:
            context['is_empty'] = True
        # render sidebar template
        output = nodelist.render(context)
        context.pop()
        return output


def do_section_sidebar(parser, token):
    """
    {% sidebar section_obj issue_obj num %}
    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise template.TemplateSyntaxError, "%s takes three arguments" % bits[0]
    return SidebarItemsByIssueNode(bits[1], bits[2], bits[3])
register.tag('sidebar', do_section_sidebar)

##def news_sidebar(num):
##    params = {}
##    params['items'] = NewsCalendarItem.objects.filter(start_time__gte=datetime.now())[:num]
##    if len(list(params['items'])) == 0:
##        params['is_empty'] = True
##    return params
##
##
##def arts_sidebar(num):
##    params = {}
##    params['items'] = ArtsCalendarItem.objects.filter(start_time__gte=datetime.now())[:num]
##    if len(list(params['items'])) == 0:
##        params['is_empty'] = True
##    return params

##register.inclusion_tag('sidebars/news_sidebar.html')(news_sidebar)
##register.inclusion_tag('sidebars/arts_sidebar.html')(arts_sidebar)
