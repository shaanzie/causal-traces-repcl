import datetime as dt
from math import floor
import random
from copy import deepcopy

class HVC: 

    def __init__(self, times: list, epsilon: int, epoch_interval: int, pid: int, max_procs: int) -> None:
        
        self.interval = epoch_interval
        self.max_epoch = 0
        self.times = times
        self.epsilon = epsilon
        self.counters = [0]*max_procs
        self.offsets = [-epsilon]*max_procs
        self.pid = pid
        self.max_procs = max_procs
        for idx in range(len(times)):
            self.offsets[idx] = min(abs(self.max_epoch - times[idx]), epsilon)
        self.offsets[self.pid] = 0

        self.local_event_probability = 1


    def __repr__(self) -> str:
        
        return 'HVC(clock_pid={pid}, \nmax_epoch={max_epoch}, \ncounters={counters}, \noffsets={offsets}'.format(
            pid = self.pid,
            max_epoch = self.max_epoch, 
            counters = self.counters, 
            offsets = self.offsets
        )

    def get_offset_size(self) -> str:

        return sum((abs(x) < self.epsilon) for x in self.offsets) - 1
    
    def get_counter_size(self) -> str:
        
        return sum(x > 0 for x in self.counters)

    def get_perceived_e_drift(self) -> str:

        max_drift = 0

        for pid1 in range(self.max_procs):
            for pid2 in range(self.max_procs):
                drift = self.offsets[pid2] - self.offsets[pid1]
                if abs(drift) < self.epsilon and abs(drift) > max_drift:
                    max_drift = drift

        return max_drift 


    def as_list(self) -> list:

        vector_clock = [0]*self.max_procs
        for pid in range(self.max_procs):
            vector_clock[pid] = self.max_epoch + self.offsets[pid] + (self.counters[pid] / self.max_procs)
        return vector_clock

    def __eq__(self, other: 'HVC') -> bool:
        return self.as_list() == other.as_list()

    def __ne__(self, other: 'HVC') -> bool:
        return self.as_list() != other.as_list()

    def __lt__(self, other: 'HVC') -> bool:
        self_vc = self.as_list()
        other_vc = other.as_list()
        for idx in range(self.max_procs):
            if self_vc[idx] >= other_vc[idx]:
                return False

    def __le__(self, other: 'HVC') -> bool:
        self_vc = self.as_list()
        other_vc = other.as_list()
        for idx in range(self.max_procs):
            if self_vc[idx] > other_vc[idx]:
                return False

    def __gt__(self, other: 'HVC') -> bool:
        self_vc = self.as_list()
        other_vc = other.as_list()
        for idx in range(self.max_proc):
            if self_vc[idx] <= other_vc[idx]:
                return False

    def __ge__(self, other: 'HVC') -> bool:
        self_vc = self.as_list()
        other_vc = other.as_list()
        for idx in range(self.max_procs):
            if self_vc[idx] < other_vc[idx]:
                return False
    
    def find_system_epoch(self):

        return dt.datetime.now(dt.timezone.utc).time()
        
    def advance(self, phy_clock: int):
        
        # print('\nAdvancing..')
        # system_epoch = self.find_system_epoch()
        new_max_epoch = max(self.max_epoch, floor(phy_clock / self.interval))

        if(new_max_epoch == self.max_epoch):
            # print('Max epoch matches, advancing counter')
            self.counters[self.pid] += 1
        
        else:
            # print('Max epoch does not match, resetting counters and offsets')
            self.counters = [0]*self.max_procs
            for idx in range(self.max_procs):
                if(self.offsets[idx] != self.epsilon):
                    self.offsets[idx] = min(self.offsets[idx] + new_max_epoch - self.max_epoch, self.epsilon)

        self.max_epoch = new_max_epoch
        self.offsets[self.pid] = 0
        
    def merge(self, m: 'HVC', phy_clock: int):

        # print('\nMerging clocks')
        # system_epoch = self.find_system_epoch()
        new_max_epoch = max(self.max_epoch, floor(phy_clock / self.interval), m.max_epoch) 

        if new_max_epoch == self.max_epoch and new_max_epoch == m.max_epoch:
            for pid in range(self.max_procs):
                self.counters[pid] = max(self.counters[pid], m.counters[pid])
            self.counters[self.pid] = max(self.counters[self.pid], m.counters[self.pid]) + 1
            self.offsets[m.pid] = 0

        elif new_max_epoch == self.max_epoch:
            # print('Max epoch unchanged, resetting offsets')
            self.counters[self.pid] += 1
            self.offsets[m.pid] = floor(min(self.max_epoch - m.max_epoch, self.epsilon))

        elif new_max_epoch == m.max_epoch:
            # print('Max epoch changed to message, resetting clock')
            self.offsets = m.offsets
            self.counters = m.counters
            self.counters[self.pid] += 1
            self.max_epoch = m.max_epoch

        else:
            # print('System clock changed max epoch, just advancing')
            self.advance(phy_clock=phy_clock)

        self.offsets[self.pid] = 0


if __name__ == '__main__':

    # clock1 = HVC([10, 10, 10], 10, 10, 0, 3)
    # clock2 = HVC([10, 10, 10], 10, 10, 1, 3)
    # clock3 = HVC([10, 10, 10], 10, 10, 2, 3)

    def print_clock(clock: HVC):

        print('{clock} for process {pid}'.format(clock = clock, pid = clock.pid))

    # clock1.max_epoch = 60
    # clock1.offsets = [0, 2, 3]
    # clock1.counters = [2, 0, 0]
    
    # clock2.max_epoch = 60
    # clock2.offsets = [1, 0, 5]
    # clock2.counters = [1, 2, 0]

    # clock1.merge(clock2, 0)
    # print_clock(clock1)

    # clock2.max_epoch = 60
    # clock2.offsets = [1, 0, 5]
    # clock2.counters = [1, 5, 3]

    # clock1.merge(clock2, 0)

    # print_clock(clock1)

    # clock1.advance(1)

    # print_clock(clock1)

    # clock2.advance(61)
    
    # print_clock(clock1)

    # clock1.merge(clock2, 0)
    
    # print_clock(clock1)

    # Implement time leader
    # Email Duong for client server setting tests
    # DKBF - designed by Muhammad for Client server tests (Google protocol for marshalling) - thesis

    clock1 = HVC([0, 0], 2, 10, 0, 2)
    print_clock(clock1)

    clock1.advance(1)
    print_clock(clock1)