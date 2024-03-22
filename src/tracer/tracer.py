from event.event import Event

class Tracer:

    def __init__(self, trace: list[Event]) -> None:
        
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
                if send_event.sender == recv_event.receiver and send_event.receiver == recv_event.sender and send_event.event_time <= recv_event.event_time:
                    send_event.event_id = event_id
                    recv_event.event_id = event_id
                    event_id += 1

        matched_events = sends.append(recvs)

        print('Events matched.')

        return matched_events


    def order_events(self):

        print('Ordering events...')
        
        events = self.match_sends_and_recvs()
        sorted_events = sorted(events)

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


    def start_tracing(self) -> None:
        pass