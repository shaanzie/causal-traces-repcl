import multiprocessing
import time
import random
import hvc
import argparse
import time

parser = argparse.ArgumentParser(
    description='Program to simulate a distributed system using HVC')

# Add named arguments
parser.add_argument('-n', '--num_procs', type=int,
                    help='Number of processes in the system')
parser.add_argument('-d', '--delta', type=int,
                    help='Maximum transmission delay')
parser.add_argument('-e', '--epsilon', type=int, help='Clock skew')
parser.add_argument('-a', '--alpha', type=int, help='Message rate')
parser.add_argument('-i', '--interval', type=int, help='Epoch interval')

args = parser.parse_args()

# Define the number of processes in the system
NUM_PROCESSES = args.num_procs

# Define the rate at which messages will be sent (in seconds)
ALPHA = args.alpha / 1000

# Define the transmission delay for each message (in seconds)
DELTA = args.delta

# Define clock skew in the system (in seconds)
EPSILON = args.epsilon

# Define interval for the epochs (in seconds)
INTERVAL = args.interval


# Define a function to simulate a message being sent from one process to another


def send_message(queue, clock, sys_clock, source, destination):

    # Get current time
    skews = [random.random() for i in range(NUM_PROCESSES)]
    sys_clock[source] += skews[source]
    clock[source].advance(sys_clock[source])

    # Simulate a delay before the message arrives at the destination process
    time.sleep(DELTA)
    # Put the message in the destination process's message queue
    queue[destination].put(clock[source])

# Define a function to simulate a process sending messages at a predefined rate


def simulate_process(queue, clock, sys_clock, process_id):
    while True:
        if (random.random() > 0.5):
            # Choose a random destination process to send a message to
            dest = random.choice(range(NUM_PROCESSES))
            # Send the message
            send_message(queue, clock, sys_clock, process_id, dest)
            # Wait for the specified message rate before sending the next message
            time.sleep(ALPHA)
        else:
            skews = [1 + random.random() for i in range(NUM_PROCESSES)]
            sys_clock[process_id] += skews[process_id]
            clock[process_id].advance(sys_clock[process_id])

# Function to get the offsize of the HVC


def get_HVC_off_size(clock: hvc.HVC):

    return len(clock.offsets.keys())

# Function to get the cousize of the HVC


def get_HVC_cou_size(clock: hvc.HVC):

    return len(clock.counters.keys())


# Create a message queue for each process
queues = [multiprocessing.Queue() for _ in range(NUM_PROCESSES)]
clocks = [hvc.HVC(interval=INTERVAL, pid=i, epsilon=EPSILON)
          for i in range(NUM_PROCESSES)]
sys_clocks = [0 for i in range(NUM_PROCESSES)]

# Create a process for each process in the system
processes = []
for i in range(NUM_PROCESSES):
    process = multiprocessing.Process(
        target=simulate_process, args=(queues, clocks, sys_clocks, i))
    process.start()
    processes.append(process)

# Listen for messages in each process's queue and print them out
while True:
    for i in range(NUM_PROCESSES):
        while not queues[i].empty():
            message = queues[i].get()
            skews = [random.random() for i in range(NUM_PROCESSES)]
            sys_clocks[i] += skews[i]
            clocks[i].merge(message, sys_clocks[i])
            print('{EPSILON},{INTERVAL},{DELTA},{ALPHA},{OFFSIZE},{COUSIZE},{EPOCH}'.format(
                EPSILON=EPSILON, INTERVAL=INTERVAL, DELTA=DELTA, ALPHA=ALPHA, OFFSIZE=get_HVC_off_size(clocks[i]), COUSIZE=get_HVC_cou_size(clocks[i]), EPOCH=clocks[i].max_epoch))
