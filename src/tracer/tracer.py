import json
import requests

url = 'http://127.0.0.1:8050/add'

class Tracer:

    def __init__(self, trace: list) -> None:
        
        self.trace = trace
        print('Tracer initialized.')

    def order_events(self):

        print('Ordering events...')
        
        sorted_events = sorted(self.trace)

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

        print('Events ordered.')
        
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