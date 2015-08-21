import os
import sys
import lxml.html
from lxml.cssselect import CSSSelector

fn = sys.argv[-1]
full_fn = os.path.abspath(fn)
full_dir = os.path.dirname(full_fn)
target_fn = os.path.join(full_dir, 'out.html')

with open(full_fn, 'rb') as fp:
    root = lxml.html.fromstring(fp.read())

selector = CSSSelector('li.topicref a')

for node in selector(root):
    href = node.attrib['href']
    print href

    with open(os.path.join(full_dir, href), 'rb') as fp:
        sub_node = lxml.html.fromstring(fp.read())
    sub_body = sub_node.find('body')
    sub_body.tag = 'article'
    node.getparent().replace(node, sub_body)

with open(target_fn, 'wb') as fp:
    fp.write(lxml.html.tostring(root))
