from copy import deepcopy
import json
from utils.utils import get_equal_events, get_next_event_list, sort_event_list, sort_node_events

from event.event import Event

class CandidateTraces:

    def __init__(self) -> None:
        
        print('Candidate Tracer initialized.')

    
    
    # Generate LHS trace
    def generate_bug_depth_2_lhs(self, events: dict) -> list:

        lhs_trace = []

        # Call by value
        replayEvents = deepcopy(events)

        # Get initial nextEvent
        nextEvent = get_next_event_list(replayEvents)

        while len(nextEvent) != 0:

            # Sort nextEvent
            sortedNextEvent = sort_event_list(nextEvent)

            # Get equalEvents
            equalEvents = get_equal_events(sortedNextEvent)

            # Append leftmost event
            lhs_trace.append(equalEvents[0].jsonify())

            # Remove event from nextEvent
            nextEvent.remove(equalEvents[0])

            # Remove event from replayEvents
            nodeId = equalEvents[0].event_time.nodeId
            replayEvents[nodeId].remove(equalEvents[0])

            # Add the next event from node
            if len(replayEvents[nodeId]) != 0:
                nextEvent.append(replayEvents[nodeId][0])

        return lhs_trace
    
    # Generate RHS trace
    def generate_bug_depth_2_rhs(self, events: dict) -> list:

        rhs_trace = []

        # Call by value
        replayEvents = deepcopy(events)

        # Get initial nextEvent
        nextEvent = get_next_event_list(replayEvents)

        while len(nextEvent) != 0:

            # Sort nextEvent
            sortedNextEvent = sort_event_list(nextEvent)

            # Get equalEvents
            equalEvents = get_equal_events(sortedNextEvent)

            # Append leftmost event
            rhs_trace.append(equalEvents[-1].jsonify())

            # Remove event from nextEvent
            nextEvent.remove(equalEvents[-1])

            # Remove event from replayEvents
            nodeId = equalEvents[-1].event_time.nodeId
            replayEvents[nodeId].remove(equalEvents[-1])

            # Add the next event from node
            if len(replayEvents[nodeId]) != 0:
                nextEvent.append(replayEvents[nodeId][0])

        return rhs_trace
    

    # Remove events out of cwnd
    def remove_cwnd_equal_events(self, event_list: list, cwnd: int):

        def within_window(event_1: Event, event_2: Event, cwnd: int):

            return (abs(event_1.event_time.hlc - event_2.event_time.hlc) <= cwnd)
        
        sampled_event = event_list[0]

        for event in event_list:
            if not within_window(event, sampled_event, cwnd):
                event_list.remove(event)

        return event_list

    # Generate all possible traces in a cwnd
    def generate_bug_depth_c(self, events: dict, cwnd: int) -> list:

        # Getting all possible paths through DFS
        def dfs(events: dict, path: list, ne: list, cwnd: int):

            # Call by value
            replayEvents = deepcopy(events)
            nextEvent = deepcopy(ne)

            # If nextEvent is empty, we have reached a leaf
            if len(nextEvent) == 0:
                all_traces.append(path)
                return 

            # If nextEvent is not empty, sort it first
            sortedNextEvent = sort_event_list(nextEvent)

            # Get equalEvents
            equalEvents = get_equal_events(sortedNextEvent)

            # Remove events out of cwnd
            cwndEqualEvents = self.remove_cwnd_equal_events(equalEvents, cwnd)

            # Iterate through each equalEvent and consider each choice
            for event_choice in cwndEqualEvents:

                # Try each choice
                path.append(event_choice.jsonify())

                # Remove choice from nextEvent
                nextEvent.remove(event_choice)

                # Remove choice from replayEvents
                nodeId = event_choice.event_time.nodeId
                replayEvents[nodeId].remove(event_choice)

                # Add next event
                if len(replayEvents[nodeId]) != 0:
                    nextEvent.append(replayEvents[nodeId][0])

                # DFS on the choice
                dfs(replayEvents, path, nextEvent, cwnd)


        all_traces = []

        # Call by value
        replay_events = deepcopy(events)

        # Get initial nextEvent
        nextEvent = get_next_event_list(replay_events)

        dfs(replay_events, [], nextEvent, cwnd)

        return all_traces


    def generate_candidate_traces(self, events: dict, c: int, epsilon: int):
        
        trace_json = dict()
        trace_json['bug_depth_2'] = {}
        trace_json['bug_depth_c'] = {}

        trace_json['bug_depth_2']['lhs'] = self.generate_bug_depth_2_lhs(events)

        trace_json['bug_depth_2']['rhs'] = self.generate_bug_depth_2_rhs(events)

        candidate_traces = self.generate_bug_depth_c(events, c*epsilon)
        
        trace_json['bug_depth_c']['trace_list'] = candidate_traces
        trace_json['bug_depth_c']['c'] = c*epsilon
        trace_json['bug_depth_c']['n'] = len(candidate_traces)

        trace_file = open('candidate_traces.json', 'w')
        trace_file.write(json.dumps(trace_json))