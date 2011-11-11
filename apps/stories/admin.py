import datetime
from django import forms
from django.contrib import admin
from django.forms.models import BaseInlineFormSet
import settings
from stories.models import Story, StoryPhoto, StoryAuthor, Photo, FeaturedPhoto
from inlines.models import Factbox, Document, StoryPoll
from galleries.models import Gallery
from tagging.models import Tag, TaggedItem

class GalleryFormSet(BaseInlineFormSet):
    def get_queryset(self):
        return super(GalleryFormSet, \
            self).get_queryset().filter(pub_date__gt=(datetime.datetime.now() \
            - datetime.timedelta(weeks=8)))

class GalleryInline(admin.TabularInline):
    model = Gallery
    formset = GalleryFormSet
    filter_horizontal = ['images']
    extra = 1

class FactboxInline(admin.TabularInline):
    model = Factbox
    extra = 1

class DocumentInline(admin.TabularInline):
    model = Document
    extra = 1

class StoryPollInline(admin.TabularInline):
    model = StoryPoll
    extra = 1

class StoryPhotoInline(admin.TabularInline):
    model = StoryPhoto

    def formfield_for_dbfield(self, field, **kwargs):
        if field.name == 'photo':
            # Note - get_object hasn't been defined yet
            parent_story = self.get_object(kwargs['request'], Story)
            incl_photos = Photo.objects.exclude(creation_date__lt=(datetime.datetime.now() \
                - datetime.timedelta(weeks=8)))
            return forms.ModelChoiceField(queryset=incl_photos)
        return super(StoryPhotoInline, self).formfield_for_dbfield(field, **kwargs)

    def get_object(self, request, model):
        object_id = request.META['PATH_INFO'].strip('/').split('/')[-1]
        try:
            object_id = int(object_id)
        except ValueError:
            return None
        return model.objects.get(pk=object_id)

class StoryAuthorInline(admin.TabularInline):
    model = StoryAuthor

class StoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['head', 'deck', 'slug', 'tags', 'summary']}),
        ('Date information', {'fields': ['pub_date']}),
        ('Content', {'fields': ['content', 'show_headshots'], 'classes': ['richedit']}),
        ('Organizational', {'fields': ['status', 'section', 'issue', 'featured',]})
    ]
    inlines = [
        StoryPhotoInline,
        StoryAuthorInline,
        FactboxInline,
        DocumentInline,
        StoryPollInline,
        GalleryInline,
    ]
    prepopulated_fields = {'slug': ('head',),}
    list_display = ('head', 'summary', 'pub_date', 'issue', 'section', 'featured', 'status', 'pk')
    list_filter = ['pub_date', 'section', 'status', 'issue']
    search_fields = ['head', 'deck', 'content']
    actions = ['make_published', 'make_featured', 'remove_featured', 'make_draft']

    class Media:
        js = (settings.MEDIA_URL + 'js/admin/formatting-controls.js',)

    def make_published(self, request, queryset):
        rows_updated = queryset.update(status='p')
        if rows_updated == 1:
            message_bit = "1 story was"
        else:
            message_bit = "%s stories were" % rows_updated
        self.message_user(request, "%s successfully marked as published." % message_bit)
    make_published.short_description = "Mark selected stories as published"

    def make_draft(self, request, queryset):
        rows_updated = queryset.update(status='d')
        if rows_updated == 1:
            message_bit = "1 story was"
        else:
            message_bit = "%s stories were" % rows_updated
        self.message_user(request, "%s successfully marked as draft." % message_bit)
    make_draft.short_description = "Mark selected stories as draft"

    def make_featured(self, request, queryset):
        rows_updated = queryset.update(featured=True)
        if rows_updated == 1:
            message_bit = "1 story was"
        else:
            message_bit = "%s stories were" % rows_updated
        self.message_user(request, "%s successfully marked as featured." % message_bit)
    make_featured.short_description = "Mark selected stories as featured"

    def remove_featured(self, request, queryset):
        rows_updated = queryset.update(featured=False)
        if rows_updated == 1:
            message_bit = "1 story was"
        else:
            message_bit = "%s stories were" % rows_updated
        self.message_user(request, "%s successfully removed from featured." % message_bit)
    remove_featured.short_description = "Remove selected from featured"

admin.site.register(Story, StoryAdmin)

class PhotoAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['photo', 'name', 'storyphoto__story__head']
    list_display = ('name', 'issue', 'photographer', 'thumbnail', 'caption', 'photo_stories')

admin.site.register(Photo, PhotoAdmin)

class FeaturedPhotoAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(FeaturedPhoto, FeaturedPhotoAdmin)

class MyTagAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ('name',)

# Override Taggit's admin
admin.site.unregister(Tag)
admin.site.register(Tag,MyTagAdmin)
