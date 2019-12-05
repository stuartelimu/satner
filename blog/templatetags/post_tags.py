from django import template
from django.utils.safestring import mark_safe
import markdown

import bs4
import requests

WPM = 200
WORD_LENGTH = 5

register = template.Library()

def markdown_format(text):
    return mark_safe(markdown.markdown(text, extensions=['markdown.extensions.fenced_code',]))

register.filter('markdown', markdown_format)

def extract_text(url):
    html = requests.get(url).content
    soup = bs4.BeautifulSoup(html, 'html.parser')
    texts = soup.findAll(text=True)
    return texts

def is_visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif isinstance(element, bs4.element.Comment):
        return False
    elif element.string == "\n":
        return False
    return True

def filter_visible_text(page_texts):
    return filter(is_visible, page_texts)

def count_words_in_text(text_list, word_length):
    total_words = 0
    for current_text in text_list:
        total_words += len(current_text)/word_length
    return total_words

@register.simple_tag(takes_context=True)
def estimate_reading_time(context, url):
    request = context['request']
    # url = context['post'].get_absolute_url()
    post_url = request.build_absolute_uri(url)
    texts = extract_text(post_url)
    filtered_text = filter_visible_text(texts)
    total_words = count_words_in_text(filtered_text, WORD_LENGTH)
    return total_words/WPM