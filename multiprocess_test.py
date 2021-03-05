from multiprocessing import Process, Lock
from multiprocessing.sharedctypes import Value, Array
from ctypes import Structure, c_double
import numpy as np
import ctypes

class Point(Structure):
    _fields_ = [('x', c_double), ('y', c_double)]
#     _fields_ = np.array([[1.875,-6.25], [-5.75,2.0], [2.375,9.5]])

def modify(n, x, s, A):
    n.value **= 2
    x.value **= 2
    s.value = s.value.upper()
    for a in A:
        a.x **= 2
        a.y **= 2

if __name__ == '__main__':
    lock = Lock()

    n = Value('i', 7)
    x = Value(c_double, 1.0/3.0, lock=False)
    s = Array('c', b'hello world', lock=lock)
    arr = np.array([[1.875,-6.25], [-5.75,2.0], [2.375,9.5]])
    arr = ((1.875,-6.25), (-5.75,2.0), (2.375,9.5))
    arr = np.array(arr)
    print(arr.shape)
    tup = tuple(map(tuple, arr))
    A = Array(Point, tup, lock=lock)

    p = Process(target=modify, args=(n, x, s, A))
    p.start()
    p.join()

    print(n.value)
    print(x.value)
    print(s.value)
    print([(a.x, a.y) for a in A])

# # import multiprocessing
# import time
# from multiprocessing import Process, Value, Array

# class A():
#     def __init__(self):
#         pass

#     def f(self,n, a):
#         for bb in range(100):
#             n.value = 3.1415927 + bb
#             time.sleep(.1)
#             for i in range(len(a)):
#                 a[i] = -a[i]

#     def run(self):
#         self.num = Value('d', 0.0)
#         self.arr = Array('i', range(10))
#         self.p = Process(target=self.f, args=(self.num, self.arr))
#         self.p.start()


# if __name__ == '__main__':
#     myA = A()
#     myA.run()
#     for i in range(10):
#         print(myA.num.value)
#         print(myA.arr[:])
#         time.sleep(1)

# def worker(procnum, return_dict):
#     """worker function"""
#     time.sleep(procnum)
#     print(str(procnum) + " represent!")
#     return_dict[procnum] = procnum


# if __name__ == "__main__":
#     manager = multiprocessing.Manager()
#     return_dict = manager.dict()
#     jobs = []
#     for i in range(5):
#         p = multiprocessing.Process(target=worker, args=(i, return_dict))
#         jobs.append(p)
#         p.start()

#     for proc in jobs:
#         proc.join()
#         print(return_dict.values())
#         # time.sleep(1)

# 

# class A(object):
#     def __init__(self, *args, **kwargs):
#         # do other stuff
#         self.starttime = time.time()
#         self.time = self.starttime
#         self.manager = multiprocessing.Manager()
#         self.return_dict = self.manager.dict()

#     def do_something(self, i,thetime):
#         for i in range(1000):
#             thetime = time.time() - self.starttime
#             time.sleep(0.01)
#             # print('%s * %s = %s' % (i, i, i*i))


#     def run(self):
#         processes = []

#         # for i in range(10):
#         thetime = 0
#         p = multiprocessing.Process(target=self.do_something, args=(5,thetime))
#         p.start()
#         #     processes.append(p)

#         # [x.start() for x in processes]


# if __name__ == '__main__':
#     a = A()
#     a.run()
#     print('post run')
#     for i in range(10):
#         print(a.time)
#         time.sleep(1)