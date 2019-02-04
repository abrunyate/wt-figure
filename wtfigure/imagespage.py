#We want to define a subclass of Page that comes with a set of SmartImages.
#  each image is to be identified by its handle, a string.

#We need to do some magic here, because Django does. In particular, we need a
#  metaclass that along with defining a model also defines a model for the
#  images associated to the it.

from django.db import models
from django.db.models.base import ModelBase   #Django's  magic metaclass

from modelcluster.fields import ParentalKey

from smart_images.models import SmartImage

from wagtail.core.models import Page

from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel

image_class_metaclass = type(models.Model)

class ImageClassBase(models.Model):

  class Meta:
    abstract = True

  image = models.ForeignKey(
    'smart_images.SmartImage', on_delete=models.CASCADE, related_name='+'
  )
  handle = models.CharField(blank=True, max_length=250)

  panels = [
    ImageChooserPanel('image'),
    FieldPanel('handle'),
  ]

class ImagesPageMetaclass(type(Page)):
  #TODO: I'm not sure what Django uses the kwargs for.
  def __new__(cls, name, bases, attrs, **kwargs):
    #The reverse lookup name from pages to images.
    relname = '{}_images'.format(name)

    #Check if we're making an abstract class. If so no work to be done?
    try:
      if attrs["Meta"].abstract:
        return super().__new__(cls, name, bases, attrs, **kwargs)
    except KeyError:
      pass

    #Save because Django will stomp on it
    image_class_attrs = {
                         "__module__": attrs["__module__"],
                        } 

    #Make the requested class to touch up later.
    if "images" in attrs:
      raise KeyError("ImagesPageBase already define 'images'. Please use another name.")
    attrs["images"] = lambda self: getattr(self, relname)
    new_class=super().__new__(cls, name, bases, attrs, **kwargs)

    #Make an attribute dict and define the image class
    image_class_name = name+"_Image"
    page_fk = ParentalKey(new_class,
                          on_delete=models.CASCADE,
                          related_name = relname
                         )
    image_class_attrs["page"] = page_fk
    image_class = image_class_metaclass( image_class_name,
                                         ( ImageClassBase, ),
                                         image_class_attrs
                                       )

    #Fix up the new class before returning it
    images_panel = InlinePanel(relname, label="Cited images")
    new_class.content_panels = new_class.content_panels + [ images_panel ]
    return new_class

class ImagesPage(Page, metaclass=ImagesPageMetaclass):

  class Meta:
    abstract = True

  def links(self):
    ret=''
    for im in self.images.all():
      rend=im.image.get_rendition('original')
      ret+='[{}]: {}\n'.format(im.handle, rend.url)
    return ret

  content_panels = Page.content_panels
