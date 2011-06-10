from django.db import models
import datetime
from stories.models import Story, Photo

class Gallery(models.Model):
    name = models.CharField(max_length=255)
    story = models.ForeignKey(Story)
    images = models.ManyToManyField(Photo, limit_choices_to = {'creation_date__gt': datetime.datetime.now() - datetime.timedelta(weeks=8)})

    class Meta:
        verbose_name = "Photo Gallery"
        verbose_name_plural = "Photo Galleries"
        
    def first_photo(self):
        try:
            return images[0]
        except:
            return False

    def __unicode__(self):
        return self.name
