# Author: Ishaan Lagwankar
# Month updated: Apr 2023

'''
This imports may not be necessary soon
Version checking recommended
'''
import math

'''
The HVC (Hybrid Vector Clock) is a vector clock
that enforces causality in O(number of processes
not skewed past epsilon) space. It is an improvement
on the previous implementation of vector clocks and
uses a process' physical timestamp to enforce causality.

Note: The happens before relation for this HVC is defined as
e hb f -> for all offsets e.o in e.offsets and all offsets f.o in f.offsets,
e.o <= f.o and
there is one e.o such that e.o < f.o for the same PID
If two clocks are equal, they are concurrent.
'''

'''
Initial definition of class object
We can modularize this down the line but leaving
this as a single class for now.
'''


class HVC:

    '''
    Initializes the clock parameters of epsilon, interval, offsets, counters and process ID.
    For now, this clock at the worst case stores O(n) offsets and counters, but takes must lesser
    space in practice. We only worry about the average case here.
    '''

    def __init__(
        self,
        interval: int,                  # Epoch interval
        pid: int,                       # Process ID
        # Clock skew - Ideally set by the system, but you can choose to set it if you like
        epsilon: int = math.inf,
    ) -> None:

        self.interval = interval
        self.max_epoch = 0              # Epoch of process
        self.epsilon = epsilon
        self.counters = dict()
        self.offsets = dict()
        self.pid = pid

        # My offset with respect to me is always 0
        self.offsets[self.pid] = 0

    '''
    We need a representation if we ever need to debug this. For now, this seems to work
    '''

    def __repr__(self) -> str:

        return 'HVC(clock_pid={pid}, \nmax_epoch={max_epoch}, \ncounters={counters}, \noffsets={offsets}'.format(
            pid=self.pid,
            max_epoch=self.max_epoch,
            counters=self.counters,
            offsets=self.offsets
        )

    '''
    This returns the offset dictionary size
    '''

    def get_offset_size(
        self
    ) -> str:

        return len(self.offsets.keys())

    '''
    This returns the counter dictionary size
    '''

    def get_counter_size(
        self
    ) -> str:

        return len(self.counters.keys())

    '''
    This returns the clock as a standard readable vector clock should we need it.
    This is for debug purposes only. Using this function will slow down your computation.
    '''

    def as_list(
        self,
        n_procs: int
    ) -> list:

        vector_clock = [0]*n_procs
        for pid in range(n_procs):
            vector_clock[pid] = self.max_epoch + \
                self.offsets[pid] + self.counters[pid]
        return vector_clock

    '''
    This defines the advance relation, where a clock moves forward by one timestep.
    '''

    def advance(
        self,
        # Assuming this to be a UNIX timestamp, but that can change as long as you can represent it in integers
        phy_clock: int
    ):

        # Check if the new max epoch has changed by discretizing our clock to fit the interval chosen
        new_max_epoch = max(
            self.max_epoch,
            math.floor(phy_clock / self.interval)
        )

        # If our max epoch has not changed
        if (new_max_epoch == self.max_epoch):

            # If our dictionary holds the counter or not
            if(self.pid in self.counters):
                self.counters[self.pid] += 1
            else:
                self.counters[self.pid] = 1

        # We have a new max epoch
        else:
            self.counters.clear()
            for process in list(self.offsets.keys()):
                new_offset = self.offsets[process] + new_max_epoch - self.max_epoch
                if new_offset < self.epsilon:
                    self.offsets[process] = new_offset
                else:
                    del self.offsets[process]

        self.max_epoch = new_max_epoch
        self.offsets[self.pid] = 0

    '''
    This is when we hear a new message from a process in the system
    '''

    def merge(self, m: 'HVC', phy_clock: int):

        # Check if the new max epoch has changed by discretizing our clock to fit the interval chosen and comparing the clock from m
        new_max_epoch = max(
            self.max_epoch,
            math.floor(phy_clock / self.interval),
            m.max_epoch
        )

        # If the message is in the same epoch
        if new_max_epoch == self.max_epoch and new_max_epoch == m.max_epoch:

            for key in self.counters.keys() & m.counters.keys():
                self.counters[key] = max(self.counters[key], m.counters[key])

            for key in m.counters.keys() - self.counters.keys():
                self.counters[key] = m.counters[key]

            for key in self.offsets.keys() & m.offsets.keys():
                self.offsets[key] = max(self.offsets[key], m.offsets[key])

            for key in m.offsets.keys() - self.offsets.keys():
                self.offsets[key] = m.offsets[key]

            if(self.pid in self.counters):
                self.counters[self.pid] += 1
            else:
                self.counters[self.pid] = 1

            self.offsets[m.pid] = 0

        # If the message is lagging
        elif new_max_epoch == self.max_epoch:

            if(self.pid in self.counters):
                self.counters[self.pid] += 1
            else:
                self.counters[self.pid] = 1

            msg_offset = self.max_epoch - m.max_epoch
            for key in m.offsets.keys() - self.offsets.keys():
                if m.offsets[key] + msg_offset < self.epsilon:
                    self.offsets[key] = m.offsets[key] + msg_offset

            if msg_offset < self.epsilon:
                for key in m.counters.keys() - self.counters.keys():
                    self.counters[key] = m.counters[key]

            if msg_offset < self.epsilon:
                self.offsets[m.pid] = msg_offset
            else:
                if(m.pid in self.offsets):
                    del self.offsets[m.pid]

        # If the message is leading
        elif new_max_epoch == m.max_epoch:

            msg_offset = m.max_epoch - self.max_epoch

            for key in m.counters.keys():
                self.counters[key] = m.counters[key]

            for key in self.offsets.keys():
                if self.offsets[key] + msg_offset < self.epsilon:
                    self.offsets[key] += msg_offset

            for key in m.offsets.keys():
                self.offsets[key] = m.offsets[key]

            self.max_epoch = m.max_epoch

        else:
            self.advance(phy_clock=phy_clock)

        self.offsets[self.pid] = 0
