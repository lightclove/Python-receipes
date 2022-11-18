#!/usr/bin/python
# Промежуточный вариант, надо бы допилить этот модуль. Не стал бы обращать на это внимание.
# создание XML-документа
import sys
import xml_is_sax
from xml.sax.saxutils import XMLGenerator
s = [{'age': u'70', 'surname': u'Сандерс', 'name': u'Гарланд'}, {'age': u'120', 'surname': u'Макдоналд','name': u'Роналд'}]
g = XMLGenerator(sys.stdout)
g.startDocument()
g.startElement('persons', {})
for s in persons:
    g.startElement('person', s)
    g.endElement('person')
g.endElement('persons')
g.endDocument()
