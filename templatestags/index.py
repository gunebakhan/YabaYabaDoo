from django import template
register = template.Library()

@register.filter(name='index_image')
def index_image(indexable, i):
    return indexable[i].image.url


@register.filter(name='index_url')
def index_url(indexable, i):
    return indexable[i].url

@register.filter(name='index_title')
def index_url(indexable, i):
    return indexable[i].title