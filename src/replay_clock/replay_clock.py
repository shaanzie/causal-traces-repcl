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
        self.node_maps = {
            '10.1.1.1': 'alice',
            '10.1.1.2': 'bob',
            '10.1.1.3': 'charlie',
            '10.1.1.4': 'delta',
            '10.1.1.5': 'echo',
        }

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
                vc.append(self.hlc)
            
            else:
                offset = self.offsets[index]
                index += 1
                vc.append(self.hlc + epsilon - int(offset, 2))

        return vc
    
    def __lt__(self, repcl: 'ReplayClock'):
        if(self.hlc < repcl.hlc):
            return True
        elif(self.hlc > repcl.hlc):
            return False
        else:
            for i, j in zip(self.vector_offsets, repcl.vector_offsets):
                if i > j:
                    return False
            if self.counters <= repcl.counters:
                return True
            return False

    def __gt__(self, repcl: 'ReplayClock'):
        
        if(self.hlc > repcl.hlc):
            return True
        elif(self.hlc < repcl.hlc):
            return False
        else:
            for i, j in zip(self.vector_offsets, repcl.vector_offsets):
                if i < j:
                    return False
            if self.counters >= repcl.counters:
                return True
            return False

    def __eq__(self, repcl: 'ReplayClock'):
        
        return not(self > repcl) and not(self < repcl)

    def __le__(self, repcl: 'ReplayClock'):
        return self < repcl or self == repcl

    def __ge__(self, repcl: 'ReplayClock'):
        return self > repcl or self == repcl
    
    def __repr__(self) -> str:
        
        return "[(NodeId={nodeId}, HLC={hlc}, Offsets={offsets}, Counters={counters})]".format(
            nodeId = self.nodeId,
            hlc = self.hlc,
            offsets = self.readable_offsets,
            counters = self.counters
        )
    
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