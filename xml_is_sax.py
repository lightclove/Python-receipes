#!/usr/bin/python
import xml.sax
import xml.sax.handler
import xml_gen
class MyHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        self.persons = []
    
    def startElement(self, name, attributes):
        if name == "person":
            self.name = attributes["name"]
            self.surname = attributes["surname"]
            self.age = attributes["age"]

    def endElement(self, name):
        if name == "person":
            self.persons.append({'name': self.name, 'surname':
            self.surname, 'age': self.age})

if __name__ == '__main__':
    parser = xml.sax.make_parser()
    handler = MyHandler()
    parser.setContentHandler(handler)
    parser.parse("example.xml")
    print(handler.persons)