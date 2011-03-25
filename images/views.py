from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.simple import direct_to_template
from django.views.generic.create_update import create_object
from django.template import RequestContext
from django import newforms as forms
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
                new_image.image = form.cleaned_data['image'].filename
                new_image.save_image_file(new_image.get_image_filename(),form.cleaned_data['image'].content)
                new_image.save()
                return HttpResponseRedirect(reverse('images.views.images_add_to_markup', args=[new_image.id]))
            else:
                return render_to_response('images/widget_add.html',
                                          {'form': form})
        else:
            form = ImageForm()
            return render_to_response('images/widget_add.html',
                                      {'form': form})
    else:
        return render_to_response('staff/access_denied.html',
                          {'missing': 'add photos to',
                           'staffapp': 'this entry'},
                          context_instance=RequestContext(request))        

##        return create_object(request,
##                             model=Image,
##                             template_name='images/widget_addd.html',
##                             post_save_redirect='/images/widget/markup/%(id)i/')
    

def images_list(request):
    return direct_to_template(request, template='images/widget_add.html')

def images_add_to_markup(request, image_id):
    c = {'image': Image.objects.get(pk=image_id)}
    return direct_to_template(request, template='images/widget_add_to_markup.html', extra_context=c)
