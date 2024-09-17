from processor.processor import FileProcessor
import pandas as pd

from event.event import Event
from replay_clock.replay_clock import ReplayClock

class CSVProcessor(FileProcessor):

    def __init__(self, cfg: dict) -> None:
        
        super().__init__(cfg)

    def get_event_list(self, df: pd.DataFrame) -> list:

        event_id = 0
        event_list = []

        for index, row in df.iterrows():

            if index == 0:
                continue
            
            e = Event(
                event_id=event_id,
                seqts=row['SEQTS'],
                event_type=row['MSG_TYPE'],
                event_time=ReplayClock(
                    nodeId=row['NODE_1'],
                    hlc=int(row['HLC']),
                    bitmap=row['BITMAP'],
                    offsets=row['OFFSETS'],
                    counters=int(row['COUNTERS']),
                    offset_size=int(row['MAX_OFFSET_SIZE']),
                    epsilon=int(row['EPSILON'])
                ),
                sender=row['NODE_1'],
                receiver=row['NODE_2'],
                msg_body=row['MSG_BODY']
            )
            event_list.append(e)
            event_id += 1

        return event_list

    def get_node_separated_events(self, events: list) -> dict:

        node_separated_events = dict()

        for node in self.cfg['nodes']:
            node_separated_events[node] = []

        for e in events:
            node_separated_events[e.event_time.nodeId].append(e)

        return node_separated_events

    def process_csv(self, filename: str) -> list:

        # Convert CSV to DF
        df = pd.read_csv(
            filepath_or_buffer=filename,
            dtype=str, 
            low_memory=False, 
            header=None
        )

        # Enrich columns
        df.columns = self.cfg['columns']

        # Initialize event_list
        init_events = self.get_event_list(df)

        # Create node separated logs
        node_separated_events = self.get_node_separated_events(init_events)

        return node_separated_events