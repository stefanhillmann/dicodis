from multiprocessing import Pool
from cross_validation_configuration import Configuration
import cross_validation_configuration

def f(conf):
    l = []
    l.append(conf)
    return l

if __name__ == '__main__':
    
    confis = cross_validation_configuration.getConfigurations()
    
    pool = Pool(processes=4)              # start 4 worker processes
    #result = pool.apply_async(f, [1])    # evaluate "f(10)" asynchronously
    
    #print result.get(timeout=1)           # prints "100" unless your computer is *very* slow
    
    print pool.map(f, confis)          # prints "[0, 1, 4,..., 81]"
