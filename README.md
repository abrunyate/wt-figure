### Figure extensions for Wagtail markdown.

This is a simple extension to look up unresolved reference style image links
in a markdown document in a modelcluster and render them as figures.

This code is slowly being factored out of my web site. In particular,
don't expect it to be good or even usable yet.

Still to be added in:

  * Some version of the extended image app "smart_images", which know about
    captions, authors, and licensing.

  * A standardized way of adding the SmartImage library model cluster to page
    models.
