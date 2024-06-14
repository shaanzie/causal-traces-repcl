from event.event import Event
import json

class Tracer:

    def __init__(self, trace: list) -> None:
        
        self.trace = trace

        print('Tracer initialized.')
    
    def sort_events(self):
        
        sends = list()
        recvs = list()

        print('Sorting events...')

        for event in self.trace:

            if event.event_type == 'SEND':
                sends.append(event)
            else:
                recvs.append(event)

        print('Events sorted.')
        
        return sends, recvs
    
    def match_sends_and_recvs(self):

        print('Matching sends and receives...')

        sends, recvs = self.sort_events()
        event_id = 0
        for send_event in sends:
            for recv_event in recvs:
                if send_event.sender == recv_event.receiver and send_event.receiver == recv_event.sender and send_event.event_time <= recv_event.event_time and send_event.event_id == 0 and recv_event.event_id == 0:
                    send_event.event_id = event_id
                    recv_event.event_id = event_id
                    event_id += 1
                    print('Matched {num}/{den} events...)'.format(
                        num = event_id*2,
                        den = len(sends) + len(recvs)
                    ))


        matched_events = sends.append(recvs)

        print('Events matched.')

        return matched_events


    def order_events(self):

        print('Ordering events...')
        
        sorted_events = sorted(self.trace)
        # events = self.match_sends_and_recvs()

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

        shiviz_trace = open('shiviz_trace.txt', 'w')
        

        for events in grouped_events:
            if len(events) == 1:
                print(events[0])
                json_trace['trace'].append(events[0].jsonify())
                shiviz_trace.write(events[0].shiviz_format())
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
                    shiviz_trace.write(events[event_id].shiviz_format())
        
        Trace_File = open(r'generated_trace.json', 'w')
        Trace_File.write(json.dumps(json_trace))