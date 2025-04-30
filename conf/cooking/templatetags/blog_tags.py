from django import template
from django.db.models import Count


from cooking.models import Category


register = template.Library()


@register.simple_tag()
def get_all_categories():
    return Category.objects.annotate(cnt=Count('post')).filter(cnt__gt=0)