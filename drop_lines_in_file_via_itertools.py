'''
    Итерируемые объекты

    Иногда нужно работать с файлом, который, как заранее известно,
    начинается с некоторого числа ненужных строк — вроде строк с комментариями.
    Для того чтобы пропустить эти строки, можно, снова, прибегнуть к
    возможностям itertools:

    File contents:

    String_from_file = " ... "
    // Author is ...
    // License ...
    //
    // Some unuseful info
    //
    Actual contents

'''

import itertools
for line in itertools.dropwhile(lambda line:
line.startswith("//"),String_from_file.split("\n")): print(line)
