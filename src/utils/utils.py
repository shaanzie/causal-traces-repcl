from event.event import Event
from collections import Counter

# Sort events by node
def sort_node_events(events: dict):

    for node in events.keys():

        sorted_events = sorted(events[node], key=lambda x: x.event_time)
        events[node] = sorted_events 

    return events

# Generate nextEvent list
def get_next_event_list(events: dict) -> list:

    nextEvent = [events[node][0] for node in events.keys() if len(events[node]) != 0]

    return nextEvent

# Sort event lists by RepCl
def sort_event_list(event_list: list) -> list:

    return sorted(event_list, key=lambda x: x.event_time)

# Remove events that are not equal
def get_equal_events(event_list: list):

    equal_events = [event_list[0]]

    for event in event_list:
        if event.event_time == event_list[0].event_time and event != event_list[0]:
            equal_events.append(event)

    for event_1 in equal_events:
        for event_2 in equal_events:
            if event_1.event_time > event_2.event_time:
                try:
                    equal_events.remove(event_1)
                except:
                    pass

    return equal_events

def in_window(event: Event, window_start: int, window_end: int):

    return event.event_time.hlc > window_start and event.event_time.hlc < window_end


def filter_events(replay_events: dict, window_start: int, window_end: int):

    filtered_dict = dict()

    for key in replay_events.keys():

        filtered_dict[key] = list()

        for event in replay_events[key]:

            if in_window(event, window_start, window_end):

                filtered_dict[key].append(event)

    for key in replay_events.keys():
        if key in filtered_dict:
            replay_events[key] = [item for item in replay_events[key] if item not in filtered_dict[key]]

    return filtered_dict