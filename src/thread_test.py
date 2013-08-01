from multiprocessing import Process, Lock
import time


def my_f(lock, pd):
    lock.acquire()
    print 'x: ', pd
    lock.release()

if __name__ == '__main__':
    lock = Lock()
    
    jobs = []
    for num in range(10):
        p = Process(target=my_f, args=(lock, num))
        jobs.append(p)
        
    runnig = 0
    max_running = 2
    