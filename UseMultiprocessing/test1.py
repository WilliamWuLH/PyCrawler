from multiprocessing import pool
import multiprocessing
from multiprocessing.dummy import Pool as ThreadPool
import time
from tqdm import tqdm

def fun(num):
    num = num + 1
    time.sleep(0.5)
    print('\r',num,end='')
    return num

if __name__ == '__main__':
    pool_size = multiprocessing.cpu_count()
    num_size = 10
    print('pool size : %d' % pool_size)

    #
    # sequential
    # 
    res = []
    s = time.time()
    for i in range(num_size):
        res.append(fun(i))
    e = time.time()

    print('\nsequential time : %0.3f' % (e - s))
    if num_size < 30:
        print(res)

    #
    # process : apply
    # 
    res_cur = []
    s = time.time()
    with pool.Pool(pool_size) as mypool:
        for i in range(num_size):
            res_cur.append(mypool.apply(func=fun, args=(i,)))
        mypool.close()
        mypool.join()
    e = time.time()

    print('\nprocess : apply  time : %0.3f' % (e - s))
    if num_size < 30:
        print(res_cur)
    print(res == res_cur)

    #
    # process : apply_async
    # 
    res_cur = []
    s = time.time()
    with pool.Pool(pool_size) as mypool:
        for i in range(num_size):
            res_cur.append(mypool.apply_async(func=fun, args=(i,)))
        mypool.close()
        mypool.join()
    e = time.time()

    print('\nprocess : apply_async  time : %0.3f' % (e - s))
    for i in range(len(res_cur)):
        res_cur[i] = res_cur[i].get()
    if num_size < 30:
        print(res_cur)
    print(res == res_cur)

    #
    # process : map
    # 
    s = time.time()
    with pool.Pool(pool_size) as mypool:
        res_cur = mypool.map(fun, [i for i in range(num_size)])
        mypool.close()
        mypool.join()
    e = time.time()

    print('\nprocess : map  time : %0.3f' % (e - s))
    if num_size < 30:
        print(res_cur)
    print(res == res_cur)

    #
    # process : imap
    # 
    s = time.time()
    with pool.Pool(pool_size) as mypool:
        res_cur = mypool.imap(fun, [i for i in range(num_size)])
        mypool.close()
        mypool.join()
    e = time.time()

    print('\nprocess : imap  time : %0.3f' % (e - s))
    res_cur = list(res_cur)
    if num_size < 30:
        print(res_cur)
    print(res == res_cur)

    #
    # process : imap_unordered
    # 
    s = time.time()
    with pool.Pool(pool_size) as mypool:
        res_cur = mypool.imap_unordered(fun, [i for i in range(num_size)])
        mypool.close()
        mypool.join()
    e = time.time()

    print('\nprocess : imap_unordered  time : %0.3f' % (e - s))
    res_cur = list(res_cur)
    if num_size < 30:
        print(res_cur)
    print(res == res_cur)

    #
    # thread : map
    # 
    s = time.time()
    with ThreadPool(pool_size) as mypool:
        res_cur = mypool.map(fun, [i for i in range(num_size)])
        mypool.close()
        mypool.join()
    e = time.time()

    print('\nthread : map  time : %0.3f' % (e - s))
    if num_size < 30:
        print(res_cur)
    print(res == res_cur)
    
    #
    # thread : imap
    # 
    s = time.time()
    with ThreadPool(pool_size) as mypool:
        res_it = mypool.imap(fun, [i for i in range(num_size)])
        mypool.close()
        mypool.join()
    e = time.time()

    print('\nthread : imap  time : %0.3f' % (e - s))
    res_cur = list(res_it)
    if num_size < 30:
        print(res_cur)
    print(res == res_cur)