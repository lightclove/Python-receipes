'''
    Построение круговой диаграммы с помощью Python
    Еще один способ представления данных — 
    круговая диаграмма, которую можно получить с помощью функции pie().
    А чтобы диаграмма была идеально круглой, 
    необходимо в конце добавить функцию axis() 
    со строкой equal в качестве аргумента. 
'''
import matplotlib.pyplot as plt
import numpy as numpy

labels = ['', '', '', '']
values = [10, 30, 45, 15]
colors = ['yello','green','red','blue']

plt.pie(values,labels=labels,colors=colors)
plt.axis('equal')
plt.show()
