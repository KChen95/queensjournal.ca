from django import template
from structure.models import Issue, FrontConfig
from stories.models import Story
from blog.models import Blog


register = template.Library()

def menu_sections(context):
    """
    Returns the HTML code for the sections menu of a given issue.
    """
    params = {}
    back_issue = context.get('back_issue')
    if back_issue is True:
        params['back_issue'] = back_issue
        try:
            curr_issue = FrontConfig.objects.get(issue=context.get('issue'))
        except FrontConfig.DoesNotExist:
            curr_issue = context.get('issue')
    else:
        try:
            curr_issue = FrontConfig.objects.latest('pub_date')
        except FrontConfig.DoesNotExist:
            return None
    if context.get('story_set'):
        params['show_section_link'] = False
    else:
        params['show_section_link'] = True
    params['sections'] = curr_issue.sections
    params['config'] = context.get('config')
    return params

class OtherStoriesListNode(template.Node):
    """
    Returns a list of other stories in the section for a given issue as the 'other_stories' context variable.
    """
    def __init__(self, section, issue, num=0):
        self.section, self.issue, self.num = section, issue, num

    def render(self, context):
        # first, grab actual section/issue objects from context
        try:
            section_obj = template.resolve_variable(self.section, context)
            issue_obj = template.resolve_variable(self.issue, context)
        except:
            context['no_other_stories'] = True
            return ''
        context['other_stories'] = Story.objects.filter(issue=issue_obj, section=section_obj).exclude(slug=context.get('story').slug)
        if self.num != 0:
            context['other_stories'] = context['other_stories'][:self.num]
        if len(context['other_stories']) == 0:
            context['no_other_stories'] = True
        return ''

def do_other_stories(parser, token):
    """
    {% other_stories section_obj issue_obj num %}
    """
    bits = token.contents.split()
    if len(bits) != 3 and len(bits) != 4:
        raise template.TemplateSyntaxError, "%s takes two or three arguments" % bits[0]
    if len(bits) == 4:
        return OtherStoriesListNode(bits[1], bits[2], bits[3])
    else:
        return OtherStoriesListNode(bits[1], bits[2])

def menu_blogs(context):
    '''
    Provides HTML code for active blogs
    '''
    params = {}
    params['blogs'] = Blog.objects.filter(active=True)
    return params

def menu_mobile(context):
    """
    Returns the HTML code for the sections menu of a given issue.
    """
    params = {}
    back_issue = context.get('back_issue')
    if back_issue is True:
        params['back_issue'] = back_issue
        try:
            curr_issue = FrontConfig.objects.get(issue=context.get('issue'))
        except FrontConfig.DoesNotExist:
            curr_issue = context.get('issue')
    else:
        curr_issue = FrontConfig.objects.latest('pub_date')
    if context.get('story_set'):
        params['show_section_link'] = False
    else:
        params['show_section_link'] = True
    params['sections'] = curr_issue.sections
    params['config'] = context.get('config')
    return params

register.inclusion_tag('global/menu_sections.html', takes_context=True)(menu_sections)
register.tag('other_stories', do_other_stories)
register.inclusion_tag('global/menu_blogs.html', takes_context=True)(menu_blogs)
register.inclusion_tag('global/menu.html', takes_context=True)(menu_mobile)
