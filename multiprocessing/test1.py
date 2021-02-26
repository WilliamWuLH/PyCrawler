from multiprocessing import pool
from multiprocessing.dummy import Pool as ThreadPool
import time
from tqdm import tqdm

def fun(num):
    num = num + 1
    # time.sleep(1)
    print('\r',num,end='')
    return num

if __name__ == '__main__':
    pool_size = 4
    num_size = 10000

    #
    # process : apply
    # 
    res1 = []
    s = time.time()
    pool1 = pool.Pool(pool_size)
    for i in range(num_size):
        res1.append(pool1.apply(func=fun, args=(i,)))
    pool1.close()
    pool1.join()
    e = time.time()
    print('\nprocess : apply  time : %0.3f' % (e - s))
    # print(res1)

    #
    # process : apply_async
    # 
    res2 = []
    s = time.time()
    pool2 = pool.Pool(pool_size)
    for i in range(num_size):
        res2.append(pool2.apply_async(func=fun, args=(i,)))
    pool2.close()
    pool2.join()
    e = time.time()
    print('\nprocess : apply_async  time : %0.3f' % (e - s))
    for i in range(len(res2)):
        res2[i] = res2[i].get()
    print(res1 == res2)

    #
    # thread : map
    # 
    s = time.time()
    pool3 = ThreadPool(pool_size)
    res3 = pool3.map(fun, [i for i in range(num_size)])
    pool3.close()
    pool3.join()
    e = time.time()
    print('\nthread : map  time : %0.3f' % (e - s))
    # print(res3)
    print(res1 == res3)
    
    #
    # thread : imap
    # 
    s = time.time()
    pool4 = ThreadPool(pool_size)
    res_it = pool4.imap(fun, [i for i in range(num_size)])
    pool4.close()
    pool4.join()
    e = time.time()
    print('\nthread : imap  time : %0.3f' % (e - s))
    res4 = list(res_it)
    # print(res4)
    print(res1 == res4)