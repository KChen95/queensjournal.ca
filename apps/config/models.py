from django.db import models
from solo.models import SingletonModel
from tagging.fields import TagField
from tagging.models import Tag


class SiteConfig(SingletonModel):
    '''
    Global configuration settings

    This model holds all global settings for the site, like featured stuff and
    active sections.

    Please try to keep all fields nullable, or include a default value, so the
    default instance can be created programmatically. e.g. see the .get() class
    method
    '''
    featured_tags = TagField()
    announcement_head = models.CharField(max_length=256, blank=True)
    announcement_body = models.TextField(blank=True)
    featured_video = models.ForeignKey('video.Video', blank=True, null=True,
        help_text="If this isn't set the most recent video will be used.",
        default=None)
    featured_stories = models.ManyToManyField('stories.Story',
        through='FeaturedStory')

    def get_tags(self):
        return Tag.objects.get_for_object(self)

    @classmethod
    def get(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj

    def __unicode__(self):
        return "Site Configuration"

    class Meta:
        verbose_name = "Site Configuration"


def get_previous_story_order():
    try:
        prev = FeaturedStory.objects.all()[0].id + 1
    except:
        prev = 0
    return prev


class FeaturedStory(models.Model):
    story = models.ForeignKey('stories.Story')
    config = models.ForeignKey(SiteConfig)
    orig_photo = models.ImageField("Photo", upload_to='featured_photos/%Y/%m/%d')
    story_order = models.PositiveIntegerField(help_text="Lower the number, order it will \
        show in the Front slideshow", default=get_previous_story_order, unique=True)

    class IKOptions:
    # Defining ImageKit options
        spec_module = 'stories.featured_specs'
        cache_dir = 'photo_cache'
        image_field = 'orig_photo'

    class Meta:
        verbose_name = 'Top Story'
        verbose_name_plural = 'Top Story'
        ordering = ['story__pub_date']

    def __unicode__(self):
        from django.utils.encoding import force_unicode
        return 'Featured Story: %s' % (force_unicode(self.story.head))

    def delete(self, *args, **kwargs):
        super(FeaturedStory, self).delete(*args, **kwargs)
        if self.image:
            self.image.delete()
    delete.alters_data = True
