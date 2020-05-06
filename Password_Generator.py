# -*- coding: UTF-8 -*-
# !/usr/bin/env python2

import random 
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

	x = raw_input("Введите длину пароля - количество символов ")
	print "Your password is:"
	print passw_generator(int(x)) 
except ValueError:
	print "Incorrect value, will generated random password with length of the 8 characters"
	print passw_generator() # выведет пароль из 8ми
