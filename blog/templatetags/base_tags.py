import datetime
from django import template
from .. import models

register = template.Library()


@register.simple_tag
def title():
    return "سایت اطلاع رسانی دبیرستان شهیدان احسانی"

@register.inclusion_tag('blog/partials/category_navbar.html')
def category_navbar():
    return {
        "categoryies" : models.Category.objects.all().filter(status=True),
    }

@register.inclusion_tag("registration/partials/link.html")
def link(request, link_name, content, icon_name):
      return {
          "request" : request,
          "link_name" : link_name,
          "link" : "auth:{}".format(link_name),
          "content" : content,
          "icon_name" : icon_name
      }