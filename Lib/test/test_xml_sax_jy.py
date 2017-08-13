import unittest
from test import test_support

from StringIO import StringIO

import xml.sax
import xml.sax.handler


class XmlHandler(xml.sax.ContentHandler):

    def __init__(self, root_node, connection):
        self.connection = connection
        self.nodes = [('root', root_node)]
        self.current_text = ''

    def startElement(self, name, attrs):
        self.current_text = ''
        new_node = self.nodes[-1][1].startElement(name, attrs, self.connection)
        if new_node is not None:
            self.nodes.append((name, new_node))

    def endElement(self, name):
        self.nodes[-1][1].endElement(name, self.current_text, self.connection)
        if self.nodes[-1][0] == name:
            if hasattr(self.nodes[-1][1], 'endNode'):
                self.nodes[-1][1].endNode(self.connection)
            self.nodes.pop()
        self.current_text = ''

    def characters(self, content):
        self.current_text += content


class RootElement(object):
    def __init__(self):
        self.start_elements = []
        self.end_elements = []
    def startElement(self, name, attrs, connection):
        self.start_elements.append([name, attrs, connection])

    def endElement(self, name, value, connection):
        self.end_elements.append([name, value, connection])


class JavaSaxTestCase(unittest.TestCase):

    def test_javasax_with_skipEntity(self):
        content = '<!DOCTYPE Message [<!ENTITY xxe SYSTEM "http://aws.amazon.com/">]><Message>error:&xxe;</Message>'

        root = RootElement()
        handler = XmlHandler(root, root)
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        parser.setFeature(xml.sax.handler.feature_external_ges, 0)
        parser.parse(StringIO(content))

        self.assertEqual('Message', root.start_elements[0][0])
        self.assertItemsEqual([['Message', 'error:', root]], root.end_elements)


def test_main():
    test_support.run_unittest(JavaSaxTestCase)


if __name__ == '__main__':
    test_main()
