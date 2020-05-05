#-*-coding:utf-8*-
#!/usr/bin/env python
''''''
import codecs
file = codecs.open("write_cyrillic_in_file.txt", "w", "utf-8")
file.write(u'какая-то строка')
file.close()