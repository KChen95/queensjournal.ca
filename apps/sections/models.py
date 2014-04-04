from django.db import models
from stories.models import Story


class Section(models.Model):
    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=16,
        help_text='For use in site navigation like section menus, breadcrumb, \
            etc. Optional.', blank=True, null=True)
    slug = models.SlugField()

    def __unicode__(self):
        return self.name

    def get_latest_stories(self, limit=10):
        return Story.stories.published().filter(section=self)[:limit]
