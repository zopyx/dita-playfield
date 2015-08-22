import os
import sys
import lxml.html
from lxml.cssselect import CSSSelector

fn = sys.argv[-1]
full_fn = os.path.abspath(fn)
full_dir = os.path.dirname(full_fn)
target_fn = os.path.join(full_dir, 'out.html')


def article_from_href(href):

    with open(os.path.join(full_dir, href), 'rb') as fp:
        sub_node = lxml.html.fromstring(fp.read())

    sub_body = sub_node.find('body')
    article_sub_nodes = sub_node.xpath('//article')
    if not article_sub_nodes:
        return 
    article_sub_node = article_sub_nodes[0]
    article_sub_node.attrib['id'] = sub_body.attrib['id']
    for nav in sub_body.xpath('//nav'):
        nav.getparent().remove(nav)

    return article_sub_node

def hierarchy_level(node):

    current = node
    count = 0
    while current:
        css_class = current.attrib.get('class', '')
        if 'topicref' in css_class:
            count += 1
        current = current.getparent()
    return count

with open(full_fn, 'rb') as fp:
    root = lxml.html.fromstring(fp.read())

selector = CSSSelector('li.topicref')

html = lxml.etree.Element('html')
html.append(lxml.etree.Element('head'))
body = lxml.etree.Element('body')
html.append(body)

for topicref in selector(root):
    print topicref
    first_link = topicref.find('a')
    print first_link
    topic_href = first_link.attrib['href']
    topic_title = first_link.text
    topic_level = hierarchy_level(topicref)

    print '-'*80
    print topic_href
    print topic_level
    article_node = article_from_href(topic_href)
    article_node.attrib['level'] = str(topic_level)
    body.append(article_node)

with open(target_fn, 'wb') as fp:
    fp.write(lxml.html.tostring(html))
