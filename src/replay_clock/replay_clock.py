class ReplayClock:

    def __init__(self, nodeId:int, hlc: int, bitmap: str, offsets: str, counters: int, offset_size: int, epsilon: int) -> None:

        self.nodeId = nodeId
        self.hlc = hlc
        self.bitmap = bitmap[::-1]
        self.offsets = [offsets[i:i + offset_size] for i in range(0, len(offsets), offset_size)]
        self.offsets.reverse()
        self.readable_offsets = self.convert_to_readable_offsets(offset_size=offset_size, epsilon=epsilon)
        self.counters = counters
        self.vector_offsets = self.convert_to_vector_offsets(offset_size=offset_size, epsilon=epsilon)
        self.epsilon = epsilon
        

    def convert_to_readable_offsets(self, offset_size: int, epsilon: int) -> list:

        vc = []

        index = 0
        for process in range(len(self.bitmap)):
            
            if(self.bitmap[process] == '0'):
                vc.append(-epsilon)
            
            else:
                offset = self.offsets[index]
                index += 1
                vc.append(int(offset, 2))

        return vc
    
    def convert_to_vector_offsets(self, offset_size: int, epsilon: int) -> list:

        vc = []

        index = 0
        for process in range(len(self.bitmap)):
            
            if(self.bitmap[process] == '0'):
                vc.append(self.hlc - epsilon)
            
            else:
                offset = self.offsets[index]
                index += 1
                vc.append(self.hlc - int(offset, 2))

        return vc
    
    def __lt__(self, repcl: 'ReplayClock'):
        if(self.hlc + self.epsilon < repcl.hlc):
            return True
        elif(self.hlc > repcl.hlc + self.epsilon):
            return False
        else:
            for i, j in zip(self.vector_offsets, repcl.vector_offsets):
                if i > j:
                    return False
            if self.counters < repcl.counters:
                return True
            return False

    def __gt__(self, repcl: 'ReplayClock'):
        
        if(self.hlc > repcl.hlc + self.epsilon):
            return True
        elif(self.hlc + self.epsilon < repcl.hlc):
            return False
        else:
            for i, j in zip(self.vector_offsets, repcl.vector_offsets):
                if i < j:
                    return False
            if self.counters > repcl.counters:
                return True
            return False

    def __eq__(self, repcl: 'ReplayClock'):
        
        return not(self < repcl) and not(repcl < self)
    
    def __repr__(self) -> str:
        
        return "[(NodeId={nodeId}, HLC={hlc}, Offsets={offsets}, Counters={counters})]".format(
            nodeId = self.nodeId,
            hlc = self.hlc,
            offsets = self.readable_offsets,
            counters = self.counters
        )
        # return '[VectorClock={}]'.format(self.vector_offsets)
    
    def get_human_readable_time(self) -> str:

        pt = self.vector_offsets[self.nodeId] + self.counters/10000
        return pt
    
    def jsonify(self) -> dict:

        return {
            "nodeId": self.nodeId,
            "hlc": self.hlc,
            "offsets": self.readable_offsets,
            "counters": self.counters,
            "vector_clock": self.vector_offsets
        }

    def shiviz_format(self) -> dict:
        
        vc = {}
        for i,j in zip(['alice', 'bob', 'charlie', 'delta', 'echo'], range(len(self.vector_offsets))):
            vc[i] = self.vector_offsets[j]
        return vc

if __name__ == '__main__':

    # [(HLC=10, Offsets=[e,e,1,2,e], Counters=0)]
    clock1 = ReplayClock(
        nodeId=1,
        hlc=10,
        bitmap='01100',
        offsets='00000000001000010000',
        counters=0,
        offset_size=4,
        epsilon=20
    )
    # [(HLC=10, Offsets=[e,e,0,2,e], Counters=0)]
    clock2 = ReplayClock(
        nodeId=2,
        hlc=10,
        bitmap='01100',
        offsets='00000000000000100000',
        counters=0,
        offset_size=4,
        epsilon=20
    )

    print(clock1)

    print(clock2)

    print(clock1 == clock2)