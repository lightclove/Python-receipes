#-*-coding:utf-8*-
#!/usr/bin/env python
''''''

class Person:
    def __init__(self, name):
        self.name = name

    def sayHi(self):
        print("HI! my name is", self.name)


p = Person("Dima")
p.sayHi()
print(p)
