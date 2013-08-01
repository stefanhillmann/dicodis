from multiprocessing import Process, Lock, Manager

manager = Manager()
l = manager.list()

class Foo:
    def __init__(self, bar):
        self.bar = bar

def f(lock, i):
    lock.acquire()
    foobar = Foo('foobar')
    print 'hello world', foobar
    l.append(foobar)
    lock.release()

if __name__ == '__main__':
    lock = Lock()
    
    jobs = []
    for num in range(10):
        p = Process(target=f, args=(lock, num))
        jobs.append(p)
        
    for job in jobs:
        job.start()
        
    for job in jobs:
        job.join()