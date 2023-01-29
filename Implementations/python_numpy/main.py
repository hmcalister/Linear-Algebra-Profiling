import numpy as np
import threading
import argparse

parser = argparse.ArgumentParser(
    prog="main.py",
    description="Run a linear algebra test using numpy",
)
parser.add_argument("-n",
    dest="N",
    default=100, type=int,
    help="Size of matrix and vector")

parser.add_argument("--trials", dest="trials", 
    default=1000, type=int,
    help="The number of trials to attempt")

parser.add_argument("-m", "--multiplications", dest="multiplications", 
    default=1000, type=int,
    help="The number of multiplications to use for each trial")

parser.add_argument("--threads", dest="threads", 
    default=1, type=int,
    help="The number of threads to use for each trial")

args = parser.parse_args()


num_trials_per_thread = args.trials // args.threads
matrix = np.random.normal(size=(args.N, args.N))

def heaviside(v):
    return np.sign(v)

def thread_function(thread_id, num_trials):
    for trial_index in range(num_trials):
        vector = heaviside(np.random.uniform(-1,1,size=(args.N)))
        # print(f"THREAD {thread_id}: TRIAL {trial_index}")
        for _ in range(args.multiplications):
            vector = heaviside(np.matmul(matrix,vector))


threads = [threading.Thread(target=thread_function, args=(i,num_trials_per_thread,)) for i in range(args.threads)]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
exit(0)