from replay_clock.replay_clock import ReplayClock

class Event:

    def __init__(self, event_id: int, event_type: str, event_time: ReplayClock, sender: int, receiver: int):
        
        self.event_id = event_id
        self.event_type = event_type
        self.event_time = event_time
        self.sender = sender
        self.receiver = receiver

    def __lt__(self, event: 'Event'):
        return self.event_time < event.event_time

    def __gt__(self, event: 'Event'):
        return self.event_time > event.event_time

    def __le__(self, event: 'Event'):
        return self.event_time <= event.event_time

    def __ge__(self, event: 'Event'):
        return self.event_time >= event.event_time

    def __eq__(self, event: 'Event'):
        return self.event_time == event.event_time
    
    def __repr__(self) -> str:
        return "[(EventID={event_id}, EventType={event_type}, EventTime={event_time}, Sender={sender}, Receiver={receiver})]".format(
            event_id = self.event_id,
            event_type = self.event_type,
            event_time = self.event_time,
            sender = self.sender,
            receiver = self.receiver
        )