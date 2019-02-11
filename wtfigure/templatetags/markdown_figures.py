from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

import re

register = template.Library()

#TODO: Accept single quotes.
#Groups: 0--whole tag. 1--smart_image. 2--alt text
tag_cre=re.compile(r'\{%\s*figure\s+(\S*)\s+"([^"]*)"\s*%}')

@register.filter
def link_figures(value, arg):
  def subs_fun(match):
    smart_image = arg.images().get(handle=match.group(1)).image
    return render_to_string("figure.html", {"smart_image": smart_image,
                                            "alt": match.group(2)})

  return mark_safe(tag_cre.sub(subs_fun, value))


@register.filter
def link_md(value, arg):
  return value+'\n\n'+arg.links()
