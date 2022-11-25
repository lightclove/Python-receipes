'''
You can implement queues in many ways. 
For a single machine, the standard library’s multiprocessing module 
contains a Queue function. 
Let’s simulate just a single washer and multiple dryer processes 
(someone can put the dishes away later) and an intermediate dish_queue.
'''
import multiprocessing as mp

def washer(dishes, output):
    for dish in dishes:
        print('Washing', dish, 'dish')
        output.put(dish)

def dryer(input):
    while True:
        dish = input.get()
        print('Drying', dish, 'dish')
        input.task_done()

dish_queue = mp.JoinableQueue()
dryer_proc = mp.Process(target=dryer, args=(dish_queue,))
dryer_proc.daemon = True
dryer_proc.start()
dishes = ['salad', 'bread', 'entree', 'dessert']
washer(dishes, dish_queue)
dish_queue.join()

'''
One difference between multiprocessing and threading is that threading does not
have a terminate() function. There’s no easy way to terminate a running thread, be‐
cause it can cause all sorts of problems in your code, and possibly in the space-time
continuum itself.
Threads can be dangerous. Like manual memory management in languages such as C
and C++, they can cause bugs that are extremely hard to find, let alone fix. To use threads,
all the code in the program—and in external libraries that it uses—must be thread-
safe. In the preceding example code, the threads didn’t share any global variables, so
they could run independently without breaking anything.
Imagine that you’re a paranormal investigator in a haunted house. Ghosts roam the
halls, but none are aware of the others, and at any time, any of them can view, add,
remove, or move any of the house’s contents.
You’re walking apprehensively through the house, taking readings with your impressive
instruments. Suddenly you notice that the candlestick you passed seconds ago is now
missing.
The contents of the house are like the variables in a program. The ghosts are threads in
a process (the house). If the ghosts only looked at the house’s contents, there would be
no problem. It’s like a thread reading the value of a constant or variable without trying
to change it.
Yet, some unseen entity could grab your flashlight, blow cold air down your neck, put
marbles on the stairs, or make the fireplace come ablaze. The really subtle ghosts would
change things in other rooms that you might never 
'''