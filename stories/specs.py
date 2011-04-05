# ImageKit options for story photos

from imagekit.specs import ImageSpec 
from imagekit import processors 

# first we define our thumbnail resize processor 
class ResizeThumb(processors.Resize): 
	width = 100 
	height = 100
	crop = True

# now we define a display size resize processor
class ResizeDisplay(processors.Resize):
	width = 500

class ResizeFront(processors.Resize):
	width = 225
	height = 150
	crop = True

# now lets create an adjustment processor to enhance the image at small sizes 
class EnchanceThumb(processors.Adjustment): 
	contrast = 1.2 
	sharpness = 1.1 

# now we can define our thumbnail spec 
class Thumbnail(ImageSpec): 
	access_as = 'thumbnail_image' 
	pre_cache = True
	processors = [ResizeThumb, EnchanceThumb] 

# and our display spec
class Display(ImageSpec):
	quality = 100
	processors = [ResizeDisplay]

class Front(ImageSpec):
	quality = 90
	access_as = "front_image"
	processors = [ResizeFront]