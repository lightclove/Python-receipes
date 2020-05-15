# /usr/bin/python2
# -*- coding: utf-8 -*-
########################################################################################################################
# Назначение: Труба межпроцессного взаимодействия
# Автор: https://docs.python.org/2/library/pipes.html , Дмитрий Ильюшкò ilyushko@itain.ru dm.ilyushko@gmail.com
# Создан: 15.04.2019
# Изменен: 23.07.2019
# Лицензия: MIT www.opensource.org/licenses/mit-license.php
########################################################################################################################
import pipes
t = pipes.Template()
t.append('tr a-z A-Z', '--')
f = t.open('pipefile', 'w')
f.write('hello world')
f.close()
open('pipefile').read()