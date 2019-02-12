### Figure extensions for Wagtail markdown.

This is a simple extension to look up unresolved reference style image links
in a markdown document in a modelcluster and render them as figures.

There are currently three pieces here. 
  * The markdown extension replaces unresolved image
    links `![My alt text][my_handle]` with the django-esque tag `{% figure
    my_handle "My alt text" %}`.
  * The filter `link_figures` replaces the above tag with the expansion of
    the user supplied template `figure.html`, using as context
    * `smart_image`: the image with handle `my_handle` in the
      `images` of the filter's argument.
    * `alt = "My alt text"`

    The package also provides another filter, `link_md`, that just appends
    links to the pages images to produce a self-contained standard markdown
    document.
  * An abstract parent model, `ImagesPage` for pages that have a set of
    images with handles to be used by the above process. This automatically
    produces the image container model with `ParentalKey` pointing at the page
    model and the method `Images` in the page model. The image model name is
    read from the `WAGTAILIMAGES_IMAGE_MODEL` setting.

This code is slowly being factored out of my web site. In particular,
don't expect it to be good or even usable yet.
