from django import template
from django.db.models import Count
from django.db.models import Q

from cooking.models import Category


register = template.Library()


@register.simple_tag()
def get_all_categories():
    # return Category.objects.annotate(cnt=Count('post')).filter(cnt__gt=0)
    return Category.objects.annotate(cnt=Count('post', filter=Q(post__is_published=True))).filter(cnt__gt=0)