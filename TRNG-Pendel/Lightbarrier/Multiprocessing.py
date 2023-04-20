from multiprocessing import Process, Manager
from multiprocessing import Queue
import multiprocessing
import time

def print1000(name, list):
    starttime = time.time()
    print(str(name)+" Starting "+ str(starttime))
    for i in range(1000000):
        list.append(i)
        continue
    endtime = time.time()
    print(str(name)+" Ended "+ str(endtime))
    print(str(name)+" Time:"+str((endtime-starttime)))
    
sharedList = []

if __name__ == "__main__":
    with Manager() as manager:
        sharedList = manager.list()
        sharedList2 = manager.list()

        procs = []
        first = Process(target=print1000, args=("Process1", sharedList))
        procs.append(first)
        second = Process(target=print1000, args=("Process2", sharedList2))
        procs.append(second)
        first.start()
        second.start()

        print("sleeping")
        time.sleep(4)

        print("killing")
        first.terminate()
        second.terminate()


        # for p in procs:
        #     p.join()

        print("Main")
        print(sharedList)
        print("neue Liste")
        print(sharedList2)



#print(multiprocessing.cpu_count())

# def print1000(name, stopEvent):
#     starttime = time.time()
#     print(str(name)+" Starting "+ str(starttime))
#     for i in range(10000):
#         #if(stopEvent.is_set()):
#             #break
#         continue
#     endtime = time.time()
#     print(str(name)+" Ended "+ str(endtime))
#     print(str(name)+" Time:"+str((endtime-starttime)))
    

# if __name__ == "__main__":
#     stopEvent = multiprocessing.Event()

#     first = Process(target=print1000, args=("Process1", stopEvent))
    
#     second = Process(target=print1000, args=("Process2", stopEvent))
#     first.start()
#     second.start()

#     first.join()
#     second.join()

#     print("Main")
      
