# -*- coding: UTF-8 -*-
# !/usr/bin/env python2
# Имя модуля:        
# Назначение:
# Версия интерпретатора: 2.7.15
# Автор: Дмитрий Ильюшкò ilyushko@itain.ru dm.ilyushko@gmail.com
# Создан: 
# Изменен: 
# Правообладатель: Н.А. Прохоренок ISBN-978-5-9775-0614-4 2011
# Лицензия: MIT www.opensource.org/licenses/mit-license.php


import random # Подключаем модуль random
try:
	def passw_generator (count_char=8):
		arr = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','1','2','3','4','5','6','7','8','9','0']
		passw = []
		# xrange
		for i in range(count_char):
			#  choice - выбирает произвольный символ
			passw.append(random.choice(arr))
		#print "Your generated password is: " + passw
		return "".join (passw)

	# Вызываем функцию
	# ToDo как корректно вывести кириллицу в КС
	x = raw_input("Введите длину пароля - количество символов ")
	print "Your password is:"
	print passw_generator(int(x)) # Выведет что—то вроде rPxKSlvemm
except ValueError:
	print "Incorrect value, will generated random password with length of the 8 characters"
	print passw_generator() # выведет пароль из 8ми