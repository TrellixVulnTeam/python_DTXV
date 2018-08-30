# encoding: utf-8
"""
@version:??
@author:df
"""


import os
from multiprocessing import Process, Value, Array
procs = 3
count = 0

def showdata(label, val, arr):
    msg = '%-12s:pid %4s, global: %s, value: %s, array: %s'
    print(msg %(label, os.getpid(), count, val.value, list(arr)))

def updater(val, arr):
    global count
    count += 1
    val.value += 1
    for i in range(3):
        arr[i] += 1

if __name__ == '__main__':
    scalar = Value('i',0)
    vector = Array('d',procs)
    showdata('parent start', scalar, vector)

    p = Process(target=showdata,args=('child',scalar,vector))
    p.start()
    p.join()

    print('\nloop1(updata in parent , serial, children..')

    for i in range(procs):
        count += 1
        scalar.value += 1
        vector[i] += 1
        p = Process(target=showdata, args=(('process %s' %i), scalar, vector))
        p.start()
        p.join()

    print('\nloop2(updatas in parent, parallel children)...')
    ps = []
    for i in range(procs):
        count += 1
        scalar.value += 1
        vector[i] += 1
        p = Process(target=showdata, args=(('process %s' %i), scalar, vector))
        p.start()
        ps.append(p)

    for p in ps:
        p.join()


    print('\nloop3 (updatas in serial children)...')
    for i in range(procs):
        p = Process(target=updater, args=(scalar,vector))
        p.start()
        p.join()

    showdata('perat temp',scalar,vector)

    ps = []

    print('\nloop4 ( updatas in parallel children)...')
    for i in range(procs):
        p = Process(target=updater, args=(scalar,vector))
        p.start()
        ps.append(p)
    for p in ps:
        p.join()

    showdata('parent end', scalar, vector)