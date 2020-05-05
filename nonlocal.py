#-*-coding:utf-8*-
#!/usr/bin/env python
''''''
def func_outer():
    x = 2
    print('x равно', x)
    def func_inner():
        nonlocal x
        #global x
        x = 5
    func_inner()
    print('Локальное x сменилось на', x)
func_outer()
#print(x)