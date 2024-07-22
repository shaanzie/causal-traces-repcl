import json

from numpy import equal

class Tracer:

    def __init__(self) -> None:
        
        print('Tracer initialized.')

    def order_events(self, trace: list):

        # print('Ordering events...')
        
        sorted_events = sorted(trace, key=lambda x: x.event_time)

        grouped_list = []
        current_group = []
        
        for i in range(len(sorted_events)):
            if i == 0 or sorted_events[i] != sorted_events[i-1]:
                if current_group:
                    grouped_list.append(current_group)
                    current_group = []
            current_group.append(sorted_events[i])
        
        if current_group:
            grouped_list.append(current_group)

        # print('Events ordered.')
        
        return grouped_list           


    def append_to_json_file(self, data, file_path):
        with open(file_path, 'a') as file:
            json_string = json.dumps(data)
            file.write(json_string + ',\n')


    def run_replay(self, grouped_events: list) -> None:

        json_trace = dict()
        json_trace['trace'] = []

        for events in grouped_events:
            # If event does not have any concurrent events
            if len(events) == 1:
                print(events[0])
                json_trace['trace'].append(events[0].jsonify())
                # Send request to flask to add event
                # request_data = json.dumps(events[0].jsonify())
                # response = requests.post(url=url, json=request_data)

            else:
                print("Concurrent events detected!")    
                for idx in range(len(events)):
                    print("{idx}. {event}".format(
                        idx = idx,
                        event = events[idx]
                    ))
                for idx in range(len(events)):
                    event_id = int(input('Please choose the event to replay: '))
                    print(events[event_id])
                    json_trace['trace'].append(events[event_id].jsonify())
                        
                    # Send request to flask to add event
                    # request_data = json.dumps(events[0].jsonify())
                    # response = requests.post(url=url, json=request_data)
        
        Trace_File = open(r'generated_trace.json', 'w')
        Trace_File.write(json.dumps(json_trace))

    def run_new_replay(self, trace: list) -> list:

        json_trace = dict()
        json_trace['trace'] = []

        copy_trace = trace
        while len(copy_trace) != 0:
            
            sorted_trace = sorted(copy_trace, key=lambda x: x.event_time)
            # for event in grouped_events:
            #     print(event)

            equal_events = [sorted_trace[0]]
            for event in sorted_trace:
                if event.event_time == sorted_trace[0].event_time and event != sorted_trace[0]:
                    equal_events.append(event)

            for event_1 in equal_events:
                for event_2 in equal_events:
                    if event_1.event_time > event_2.event_time:
                        equal_events.remove(event_1)

            if len(equal_events) == 1:
                print(equal_events[0])
                json_trace['trace'].append(equal_events[0].jsonify())
                # Remove first_event[0]
                copy_trace.remove(equal_events[0])

            else:
                print("Concurrent events detected!")    
                for idx in range(len(equal_events)):
                    print("{idx}. {event}".format(
                        idx = idx,
                        event = equal_events[idx]
                    ))
                event_id = int(input('Please choose the event to replay: '))
                print(equal_events[event_id])
                json_trace['trace'].append(equal_events[event_id].jsonify())
                # Remove first_event[event_id]
                copy_trace.remove(equal_events[event_id])
        
        Trace_File = open(r'generated_trace.json', 'w')
        Trace_File.write(json.dumps(json_trace))