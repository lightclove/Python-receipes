#-*-coding:utf-8*-
#!/usr/bin/env python
''''''
import os
import sys
# Функция ищет все файлы с именем filename во всех подкаталогах каталога catalog
#@ToDo сопоставить искомое выражение с регулярным
def find_files(catalog, file):
    find_files = []
    done = True
    while (done):
        print("Searching the files...Please, wait for the process to finish ")
        # Модуль os.walk() создаем объект-генератор, который выполняет обход дерева каталогов:
        for root, dirs, files in os.walk(catalog):
            find_files += [os.path.join(root, name) for name in files if name == file]
        done = False

    if not find_files: # Список не пустой
        print("Files were found:")
        for found in find_files:
            #print("File: "+ found + " were found\n")
            print(found)
    else:
        print("Files not found!")
    return find_files

#find_files(sys.argv[1], sys.argv[2])
# Для тестирования создать несколько файлов testa.txt в разных каталогах и пройтись поиском после запуска программмы
found_files_list = find_files('C:\\eric6-19.02', file='testa.txt')
# delete files
for name in found_files_list:
    os.remove(str(name))
    print("File: \"" + name + "\" were REMOVED\n")
