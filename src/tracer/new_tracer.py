import json
from copy import deepcopy
from utils.utils import sort_event_list, sort_node_events, get_equal_events, get_next_event_list

class NewTracer:

    def __init__(self) -> None:
        
        print('Tracer initialized.')

    def run_replay(self, events: dict):

        trace = []

        # Call by value
        replayEvents = deepcopy(events)

        # Get initial nextEvent
        nextEvent = get_next_event_list(replayEvents)

        while len(nextEvent) != 0:

            # Sort nextEvent
            sortedNextEvent = sort_event_list(nextEvent)

            # Get equalEvents
            equalEvents = get_equal_events(sortedNextEvent)

            if len(equalEvents) == 1:
                print(equalEvents[0])
                trace.append(equalEvents[0].jsonify())
                # Remove first_event[0]

                nodeId = equalEvents[0].event_time.nodeId
                nextEvent.remove(equalEvents[0])
                replayEvents[nodeId].remove(equalEvents[0])

                if len(replayEvents[nodeId]) != 0:
                    nextEvent.append(replayEvents[nodeId][0])

            else:
                print("Concurrent events detected!")
                for idx in range(len(equalEvents)):
                    print("{idx}. {event}".format(
                        idx = idx,
                        event = equalEvents[idx]
                    ))
                event_id = int(input('Please choose the event to replay: '))
                print(equalEvents[event_id])
                trace.append(equalEvents[event_id].jsonify())

                nodeId = equalEvents[event_id].event_time.nodeId
                nextEvent.remove(equalEvents[event_id])
                replayEvents[nodeId].remove(equalEvents[event_id])

                if len(replayEvents[nodeId]) != 0:
                    nextEvent.append(replayEvents[nodeId][0])

        Trace_File = open(r'generated_trace.json', 'w')
        Trace_File.write(json.dumps(trace))