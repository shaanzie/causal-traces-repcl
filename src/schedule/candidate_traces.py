from copy import deepcopy
import json

class CandidateTraces:

    def __init__(self) -> None:
        
        print('Candidate Tracer initialized.')

    def sort_node_events(self, events: dict):

        for node in events.keys():

            sorted_events = sorted(events[node], key=lambda x: x.event_time)
            events[node] = sorted_events 

        return events

    def generate_bug_depth_2_lhs(self, events: dict):

        lhs_trace = dict()
        lhs_trace['trace'] = []

        events = self.sort_node_events(events)

        replay_events = deepcopy(events)

        nextEvent = [replay_events[node][0] for node in replay_events.keys()]

        while len(nextEvent) != 0:

            sorted_nextEvent = sorted(nextEvent, key=lambda x: x.event_time)

            equal_events = [sorted_nextEvent[0]]

            for event in sorted_nextEvent:
                if event.event_time == sorted_nextEvent[0].event_time and event != sorted_nextEvent[0]:
                    equal_events.append(event)

            for event_1 in equal_events:
                for event_2 in equal_events:
                    if event_1.event_time > event_2.event_time:
                        equal_events.remove(event_1)

            lhs_trace['trace'].append(equal_events[0].jsonify())
            # Remove first_event[0]

            nodeId = equal_events[0].event_time.nodeId
            nextEvent.remove(equal_events[0])
            replay_events[nodeId].remove(equal_events[0])

            if len(replay_events[nodeId]) != 0:
                nextEvent.append(replay_events[nodeId][0])

        Trace_File = open(r'candidate_trace_lhs.json', 'w')
        Trace_File.write(json.dumps(lhs_trace))

    def generate_bug_depth_2_rhs(self, events: dict):

        rhs_trace = dict()
        rhs_trace['trace'] = []

        events = self.sort_node_events(events)

        replay_events = deepcopy(events)

        print(replay_events)

        nextEvent = [replay_events[node][0] for node in replay_events.keys()]

        while len(nextEvent) != 0:

            sorted_nextEvent = sorted(nextEvent, key=lambda x: x.event_time)

            equal_events = [sorted_nextEvent[0]]

            for event in sorted_nextEvent:
                if event.event_time == sorted_nextEvent[0].event_time and event != sorted_nextEvent[0]:
                    equal_events.append(event)

            for event_1 in equal_events:
                for event_2 in equal_events:
                    if event_1.event_time > event_2.event_time:
                        equal_events.remove(event_1)

            rhs_trace['trace'].append(equal_events[-1].jsonify())
            # Remove first_event[0]

            nodeId = equal_events[-1].event_time.nodeId
            nextEvent.remove(equal_events[-1])
            replay_events[nodeId].remove(equal_events[-1])

            if len(replay_events[nodeId]) != 0:
                nextEvent.append(replay_events[nodeId][0])

        Trace_File = open(r'candidate_trace_rhs.json', 'w')
        Trace_File.write(json.dumps(rhs_trace))

    def generate_candidate_traces(self, events: dict):

        self.generate_bug_depth_2_lhs(events)

        self.generate_bug_depth_2_rhs(events)