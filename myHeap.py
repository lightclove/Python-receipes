import random


class MyHeap:
    def __init__(self):
        self.heap = []
        self.size = 0

    def add(self, item):
        self.heap.append(item)
        self.size += 1
        self.siftUp(self.size-1)

    def makeHeap(self, l):
        self.heap = l
        self.size = len(l)
        for i in reversed(range(0, self.size//2)):
            self.siftDown(i)

    def siftUp(self, index):
        while index > 0 and self.heap[self.parent(index)] < self.heap[index]:
            self.heap[self.parent(
                index)], self.heap[index] = self.heap[index], self.heap[self.parent(index)]
            index = self.parent(index)

    def siftDown(self, index):
        maxIndex = index
        l = self.leftChild(index)
        if l <= self.size-1 and self.heap[l] > self.heap[index]:
            maxIndex = l
        r = self.rightChild(index)
        if r <= self.size-1 and self.heap[r] > self.heap[maxIndex]:
            maxIndex = r
        if index != maxIndex:
            self.heap[index], self.heap[maxIndex] = self.heap[maxIndex], self.heap[index]
            self.siftDown(maxIndex)

    def getTop(self):
        return self.heap[0]

    def extractTop(self):
        if self.size != 0:
            top = self.heap[0]
            self.heap[0] = self.heap[self.size-1]
            del self.heap[self.size-1]
            self.size -= 1
            self.siftDown(0)
            return top
        else:
            return False

    def remove(self, index):
        self.heap[index] = self.heap[0]+1
        self.siftUp(index)
        self.extractTop()

    def changePriority(self, index, priority):
        oldPriority = self.heap[index]
        self.heap[index] = priority
        if priority > oldPriority:
            self.siftUp(index)
        else:
            self.siftDown(index)

    def draw(self):
        lvl = []
        row1 = 0
        row2 = 0
        row3 = 0
        for i in self.heap:
            if self.heap.index(i) <= row1:
                lvl.append(i)
            else:
                print(' '*(self.size - row1), lvl)
                lvl = [i]
                if row1 == 0:
                    row2 = row1
                    row1 = 2
                else:
                    row3 = row2
                    row2 = row1
                    row1 = row2 + (row2 - row3)*2
        print(lvl)
        print('##'*row1)

    def parent(self, index):
        return (index-1)//2

    def leftChild(self, index):
        return index*2+1

    def rightChild(self, index):
        return index*2+2


H = MyHeap()
for i in range(random.randint(1, 11)):
 H.add(random.randint(1, 191))
print(H.heap)
print(H.size)
H.draw()
H.extractTop()
H.extractTop()
H.extractTop()
H.draw()

#l = [5, 2, 4, 55, 1, 2, 9, 7, 555, 99, 98, 78, 76, 565]
#H.makeHeap(l)
#H.draw()
