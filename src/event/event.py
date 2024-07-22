from replay_clock.replay_clock import ReplayClock

class Event:

    def __init__(self, event_id: int, seqts: int, event_type: str, event_time: ReplayClock, sender: int, receiver: int, msg_body: str):
        
        self.event_id = event_id
        self.seqts = seqts
        self.event_type = event_type
        self.event_time = event_time
        self.sender = sender
        self.receiver = receiver
        self.msg_body = msg_body
    
    def __repr__(self) -> str:
        return "[(EventID={event_id}, SeqTS={seqts}, EventType={event_type}, EventTime={event_time}, Sender={sender}, Receiver={receiver}, Body={msg_body})]".format(
            event_id = self.event_id,
            seqts = self.seqts,
            event_type = self.event_type,
            event_time = self.event_time,
            sender = self.sender,
            receiver = self.receiver,
            msg_body = self.msg_body
        )
    
    def jsonify(self) -> str:
        return {
            "event_id": self.event_id,
            "seqts": self.seqts,
            "event_type": self.event_type,
            "event_time": self.event_time.jsonify(),
            "node_1": self.sender,
            "node_2": self.receiver,
            "msg_body": self.msg_body
        }