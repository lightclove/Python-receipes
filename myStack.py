
class MyStack:
    def __init__(self):
        self.stack = []
        self.lenght = 0

    def add(self, value):
        self.stack.append(value)
        self.lenght += 1
        return True

    def get(self):
        assert self.lenght > 0
        if self.lenght > 0:
            value = self.stack[-1]
            del self.stack[-1]
            self.lenght -= 1
            return value
        else:
            return False

    def clear(self):
        self.stack.clear()
        self.lenght = 0

    def show(self):
        return self.stack


Q = MyStack()
Q.add(1)
Q.add(2)
Q.add(3)
Q.add(4)
Q.add(5)
Q.add(6)
Q.add(7)
Q.add(8)
print(Q.show())
print(Q.get())
print(Q.show())
Q.add(9)
print(Q.show())
print(Q.get())
print(Q.get())
print(Q.show())
print(Q.lenght)
print(Q.get())
print(Q.get())
print(Q.get())
print(Q.get())
print(Q.show())
print(Q.lenght)

