from copy import deepcopy
import json
import trace
from utils.utils import get_equal_events, get_next_event_list, sort_event_list, sort_node_events, filter_events

from event.event import Event

class CandidateTraces:

    def __init__(self) -> None:
        
        # print('Candidate Tracer initialized.')
        pass
    
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

            return (abs(event_1.event_time.hlc - event_2.event_time.hlc) <= cwnd*event_1.event_time.epsilon)
        
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
            path = deepcopy(path)

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


    def generate_bug_depth_cwnd(self, events: dict, cwnd: int, epsilon: int):

        def process_window(events: dict, window_start: int, cwnd: int, seq: int, type: int):

            # Getting all possible paths through DFS
            def dfs(replayEvents: dict, path: list, nextEvent: list):

                # If nextEvent is empty, we have reached a leaf
                if len(nextEvent) == 0:
                    window_traces.append(deepcopy(path))
                    return 
            

                # Iterate through each equalEvent and consider each choice
                for event_choice in get_equal_events(nextEvent):

                    # Try each choice
                    path.append(event_choice.jsonify())

                    # Remove choice from nextEvent
                    nextEvent.remove(event_choice)

                    # Remove choice from replayEvents
                    replayEvents[event_choice.event_time.nodeId].remove(event_choice)

                    # Add next event
                    if len(replayEvents[event_choice.event_time.nodeId]) != 0: 

                        # Get the next event from the replayEvents
                        nextEvent.append(replayEvents[event_choice.event_time.nodeId][0])
                        # If nextEvent is not empty, sort it first
                        nextEvent = sort_event_list(nextEvent)

                    # DFS on the choice
                    dfs(deepcopy(replayEvents), deepcopy(path), deepcopy(nextEvent))

                    
                    # # Restore choice from nextEvent
                    # nextEvent.append(event_choice)

                    # Restore choice from replayEvents
                    replayEvents[event_choice.event_time.nodeId].append(event_choice)
                    replayEvents[event_choice.event_time.nodeId] = sort_event_list(replayEvents[event_choice.event_time.nodeId])

                    nextEvent = get_next_event_list(replayEvents)
                    nextEvent = sort_event_list(nextEvent)

                    path.pop()


            window_traces = []

            all_traces[type] = dict()

            while(not all(value == [] for value in events.values())):
        
                filtered_events = filter_events(events, window_start, window_start + cwnd)

                nextEvent = get_next_event_list(filtered_events)

                dfs(filtered_events, [], deepcopy(nextEvent))

                window_start += cwnd

                all_traces[type][seq] = deepcopy(window_traces)

                window_traces.clear()

                seq += 1


        all_traces = dict()

        process_window(deepcopy(events), 0, cwnd*epsilon, 0, 'L')

        process_window(deepcopy(events), -(cwnd*epsilon)/2, cwnd*epsilon, 0, 'R')
        
        return all_traces
    
    def get_number_of_paths(self, traces: dict):

        n_paths = 1
        for trace in traces.values():
            n_paths *= len(trace)

        return n_paths

    def generate_candidate_traces(self, events: dict, c: int):
        
        trace_json = dict()
        trace_json['bug_depth_2'] = {}
        trace_json['bug_depth_c'] = {}

        trace_json['bug_depth_2']['lhs'] = self.generate_bug_depth_2_lhs(events)

        trace_json['bug_depth_2']['rhs'] = self.generate_bug_depth_2_rhs(events)

        event_list = get_next_event_list(events)
        epsilon = event_list[0].event_time.epsilon

        all_traces = self.generate_bug_depth_cwnd(events, c, epsilon)

        n_paths_l = self.get_number_of_paths(all_traces['L'])
        n_paths_r = self.get_number_of_paths(all_traces['R'])
        
        trace_json['bug_depth_c']['trace_list'] = all_traces
        trace_json['bug_depth_c']['cwnd'] = c*epsilon
        trace_json['bug_depth_c']['n_left'] = n_paths_l
        trace_json['bug_depth_c']['n_right'] = n_paths_r

        print('{},{},{},{}'.format(
            c,
            epsilon,
            n_paths_l,
            n_paths_r
        ))

        trace_file = open('candidate_traces.json', 'w')
        trace_file.write(json.dumps(trace_json))