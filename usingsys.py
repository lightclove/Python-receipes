#-*-coding:utf-8*-
#!/usr/bin/env python
''''''
import sys
print('Аргументы командной строки:')
for i in sys.argv:
    print(i)
print('\n\nПеременная PYTHONPATH содержит', sys.path, '\n')