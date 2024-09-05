import json

class NewTracer:

    def __init__(self) -> None:
        
        print('Tracer initialized.')

    def sort_node_events(self, events: dict):

        for node in events.keys():

            sorted_events = sorted(events[node], key=lambda x: x.event_time)
            events[node] = sorted_events

        return events

    def run_replay(self, events: dict, c: int):

        num_traces = 1
    
        json_trace = dict()
        json_trace['trace'] = []

        events = self.sort_node_events(events)

        replay_events = events

        nextEvent = [replay_events[node][0] for node in replay_events.keys()]

        while len(nextEvent) != 0:

            sorted_nextEvent = sorted(nextEvent, key=lambda x: x.event_time)

            equal_events = [sorted_nextEvent[0]]

            for event in sorted_nextEvent:
                if event.event_time <= (sorted_nextEvent[0].event_time + c) and event != sorted_nextEvent[0]:
                    equal_events.append(event)

            for event_1 in equal_events:
                for event_2 in equal_events:
                    if event_1.event_time > event_2.event_time:
                        equal_events.remove(event_1)

            if len(equal_events) == 1:
                print(equal_events[0])
                json_trace['trace'].append(equal_events[0].jsonify())
                # Remove first_event[0]

                nodeId = equal_events[0].event_time.nodeId
                nextEvent.remove(equal_events[0])
                replay_events[nodeId].remove(equal_events[0])

                if len(replay_events[nodeId]) != 0:
                    nextEvent.append(replay_events[nodeId][0])

            else:
                print("Concurrent events detected!")
                num_traces *= len(equal_events)    
                for idx in range(len(equal_events)):
                    print("{idx}. {event}".format(
                        idx = idx,
                        event = equal_events[idx]
                    ))
                event_id = int(input('Please choose the event to replay: '))
                print(equal_events[event_id])
                json_trace['trace'].append(equal_events[event_id].jsonify())
                # Remove first_event[event_id]

                nodeId = equal_events[event_id].event_time.nodeId
                nextEvent.remove(equal_events[event_id])
                replay_events[nodeId].remove(equal_events[event_id])

                if len(replay_events[nodeId]) != 0:
                    nextEvent.append(replay_events[nodeId][0])

        Trace_File = open('generated_trace_{}_{}.json'.format(c, num_traces), 'w')
        Trace_File.write(json.dumps(json_trace))