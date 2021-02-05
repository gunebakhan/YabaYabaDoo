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


@register.filter(name='get_item')
def get_item(dicti, key):
    return dicti.get(key)
    print(dicti)
    # return 1
