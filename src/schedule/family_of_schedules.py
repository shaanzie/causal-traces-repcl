class FamilyOfSchedules:

    def __init__(self) -> None:
        pass

    def generate_traces(self, node_separated_logs: dict, cwnd: int,  bug_depth: int = 2) -> list:
        
        if bug_depth == 2:
            traces = self.generate_bug_depth_2_traces(node_separated_logs)

        else:
            traces = self.generate_bug_depth_traces(node_separated_logs.copy(), cwnd)

    def generate_min_trace(self, node_separated_logs: dict) -> list:

        trace = []
            
        next_event = []
        for log in node_separated_logs.values():
            next_event.append(log[0])
    
        replayable = []
        while len(next_event) != 0:
            
            sorted_next_event = sorted(next_event, key=lambda x: x.event_time)
            replayable = [sorted_next_event[0]]

            for event in replayable:
                if event.event_time == replayable[0].event_time and event != replayable[0]:
                    replayable.append(event)

            for event_1 in replayable:
                for event_2 in replayable:
                    if event_1.event_time > event_2.event_time:
                        replayable.remove(event_1)
            
            trace.append(replayable[0])
            next_event.remove(replayable[0])

            node_id = replayable[0].sender

            del node_separated_logs[node_id][0]

            next_event.append(node_separated_logs[node_id[0]])

        return trace

    def generate_max_trace(self, node_separated_logs: dict) -> list:

        trace = []
            
        next_event = []
        for log in node_separated_logs.values():
            next_event.append(log[0])
    
        replayable = []
        while len(next_event) != 0:
            
            sorted_next_event = sorted(next_event, key=lambda x: x.event_time)
            replayable = [sorted_next_event[0]]

            for event in replayable:
                if event.event_time == replayable[0].event_time and event != replayable[0]:
                    replayable.append(event)

            for event_1 in replayable:
                for event_2 in replayable:
                    if event_1.event_time > event_2.event_time:
                        replayable.remove(event_1)
            
            trace.append(replayable[-1])
            next_event.remove(replayable[-1])

            node_id = replayable[-1].sender

            del node_separated_logs[node_id][0]

            next_event.append(node_separated_logs[node_id[0]])

        return trace

    def generate_bug_depth_2_traces(self, node_separated_logs: dict) -> list:
        
        return [self.generate_min_trace(node_separated_logs=node_separated_logs.copy()), self.generate_max_trace(node_separated_logs=node_separated_logs.copy())]

    def generate_bug_depth_traces(self, node_separated_logs: dict, cwnd: int) -> list:
        pass