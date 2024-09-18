# Sort events by node
def sort_node_events(events: dict):

    for node in events.keys():

        sorted_events = sorted(events[node], key=lambda x: x.event_time)
        events[node] = sorted_events 

    return events

# Generate nextEvent list
def get_next_event_list(events: dict) -> list:

    nextEvent = [events[node][0] for node in events.keys()]

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