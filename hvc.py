import datetime as dt
from math import floor
import random

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
        
        return 'HVC(max_epoch={max_epoch}, \ncounters={counters}, \noffsets={offsets}'.format(
            max_epoch = self.max_epoch, 
            counters = self.counters, 
            offsets = self.offsets
        )

    def get_offset_size(self) -> str:

        return sum((abs(x) < self.epsilon) for x in self.offsets) - 1
    
    def get_counter_size(self) -> str:
        
        return sum(x > 0 for x in self.counters)

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
        
        # system_epoch = self.find_system_epoch()
        new_max_epoch = max(self.max_epoch, floor(phy_clock / self.interval))

        if(new_max_epoch == self.max_epoch):
            if random.random() > self.local_event_probability:
                self.counters[self.pid] += 1
        
        else:
            self.counters = [0]*self.max_procs
            for idx in range(self.max_procs):
                pid_time = self.max_epoch - self.offsets[idx]
                self.offsets[idx] = min(new_max_epoch - pid_time, self.epsilon)

        self.max_epoch = new_max_epoch
        self.offsets[self.pid] = 0
        
    def merge(self, m: 'HVC', phy_clock: int):

        # system_epoch = self.find_system_epoch()
        new_max_epoch = max(self.max_epoch, floor(phy_clock / self.interval), m.max_epoch) 

        if new_max_epoch == self.max_epoch:
            self.counters[self.pid] += 1

        elif new_max_epoch == m.max_epoch:
            
            self.offsets = m.offsets
            self.counters = m.counters
            for idx in range(self.max_procs):
                pid_time = m.max_epoch - self.offsets[idx]
                self.offsets[idx] = min(new_max_epoch - pid_time, self.epsilon)
            self.max_epoch = m.max_epoch

        else:
            self.advance(phy_clock=phy_clock)

        self.offsets[self.pid] = 0


if __name__ == '__main__':

    clock1 = HVC([0, 0], 2, 10, 0, 2)
    clock2 = HVC([0, 0], 2, 10, 1, 2)

    def print_clock(clock: HVC):

        print('{clock} for process {pid}'.format(clock = clock, pid = clock.pid))

    clock1.advance(1)
    print('\nAdvance clock1 by 1')
    print_clock(clock1)
    clock1.advance(2)
    print('\nAdvance clock1 by 1')
    print_clock(clock1)
    clock2.advance(3)
    print('\nAdvance clock2 by 3')
    print_clock(clock2)
    clock1.advance(4)
    print('\nAdvance clock1 by 4')
    print_clock(clock1)
    clock2.merge(clock1, 4)
    print('\nMerge clock 2 with clock 1 at pt 4')
    print_clock(clock2)
    clock2.merge(clock1, 4)
    print('\nMerge clock 2 with clock 1 at pt 4')
    print_clock(clock2)
    clock2.merge(clock1, 5)
    print('\nMerge clock 2 with clock 1 at pt 5')
    print_clock(clock2)