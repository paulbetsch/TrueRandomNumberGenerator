from multiprocessing import Process, Manager
from multiprocessing import Queue
import multiprocessing
import time

# This function is just to figure out the beviour of different processes
# It is important to know when the process is being started and when it 
# finishes his tasks.
def UselessPrints(name, list):
    startTime = time.time()
    print(str(name)+" Starting "+ str(startTime))
    for i in range(1000000):
        list.append(i)
    endTime = time.time()
    print(str(name)+" Ended "+ str(endTime))
    print(str(name)+" Total Time:"+str((endTime-startTime)))
    
sharedList = []

if __name__ == "__main__":
    # Opens a new Manger to allow interprocess communication
    with Manager() as manager:
        # Two List to exchange data from the worker threads to the main threads
        sharedList = manager.list()
        sharedList2 = manager.list()

        procs = []
        first = Process(target=UselessPrints, args=("Process1", sharedList))
        procs.append(first)
        second = Process(target=UselessPrints, args=("Process2", sharedList2))
        procs.append(second)

        # Using start() to simutainiusly run the code instead of run()
        first.start()
        second.start()

        print("sleeping")
        time.sleep(4)

        # Killing the threads after 4 Seconds
        print("killing")
        first.terminate()
        second.terminate()


        # for p in procs:
        #     p.join()

        print("Main Thread")
        print(sharedList)
        print("neue Liste")
        print(sharedList2)