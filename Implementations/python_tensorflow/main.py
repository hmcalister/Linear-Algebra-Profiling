import tensorflow as tf
import threading
import argparse

parser = argparse.ArgumentParser(
    prog="main.py",
    description="Run a linear algebra test using tensorflow",
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

parser.add_argument("--batchsize", dest="batchsize", 
    default=1, type=int,
    help="The size of each batch to use in the multiplication")

args = parser.parse_args()


num_trials_per_thread = args.trials // (args.threads*args.batchsize)
matrix = tf.random.normal(shape=(1,args.N, args.N))

def heaviside(vectors):
    return tf.sign(vectors)

def thread_function(thread_id, num_trials):
    for trial_index in range(num_trials):
        vectors = tf.Variable(tf.random.normal(shape=(args.batchsize, args.N, 1)))
        vectors = heaviside(vectors)
        # print(f"THREAD {thread_id}: TRIAL {trial_index}")
        for _ in range(args.multiplications):
            vectors = heaviside(tf.matmul(matrix,vectors))

threads = [threading.Thread(target=thread_function, args=(i,num_trials_per_thread,)) for i in range(args.threads)]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
exit(0)