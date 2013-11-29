from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.views.generic.base import TemplateView
from images.models import Image
from images.forms import ImageForm

def images_add(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/staff/login/')
    elif request.user.has_perm('images.add_image'):
        if request.method == 'POST':
            form = ImageForm(request.POST, request.FILES)
            if form.is_valid():
                # save new image
                new_image = Image(name=form.cleaned_data['name'])
                if form.cleaned_data.get('caption'):
                    new_image.caption = form.cleaned_data['caption']
                if form.cleaned_data.get('credit'):
                    new_image.credit = form.cleaned_data['credit']
                new_image.image = form.cleaned_data['image']
                new_image.save()
                return HttpResponseRedirect(reverse('images.views.images_add_to_markup', args=[new_image.id]))
            else:
                return render_to_response('images/widget_add.html',
                    {'form': form},
                    context_instance=RequestContext(request))
        else:
            form = ImageForm()
            return render_to_response('images/widget_add.html',
                {'form': form},
                context_instance=RequestContext(request))
    else:
        return render_to_response('staff/access_denied.html',
            {'missing': 'add photos to',
                'staffapp': 'this entry'},
            context_instance=RequestContext(request))

##		  return create_object(request,
##							   model=Image,
##							   template_name='images/widget_addd.html',
##							   post_save_redirect='/images/widget/markup/%(id)i/')


class AddImagesView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(AddImagesView, self).get_context_data(**kwargs)
        context['image'] = Image.objects.get(pk=self.kwargs['image_id'])
        return context
