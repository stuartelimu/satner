from django import template
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

def markdown_format(text):
    return mark_safe(markdown.markdown(text, extensions=['markdown.extensions.fenced_code',]))

register.filter('markdown', markdown_format)