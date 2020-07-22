from django import template

register = template.Library()



@register.simple_tag
def get_index(post,image):
    return post.get_index(image)
