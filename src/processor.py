import pandas as pd
import base64
import io

from event.event import Event
from replay_clock.replay_clock import ReplayClock

class FileProcessor:

    def __init__(self) -> None:
        
        self.columns = [
            'MSG_TYPE',
            'NODE_1',
            'NODE_2',
            'SEQTS',
            'HLC',
            'BITMAP',
            'OFFSETS',
            'COUNTERS',
            'NUM_PROCS',
            'EPSILON',
            'INTERVAL',
            'DELTA',
            'ALPHA',
            'MAX_OFFSET_SIZE',
            'OFFSET_SIZE',
            'COUNTER_SIZE',
            'CLOCK_SIZE',
            'MAX_OFFSET',
            'MSG_BODY'
        ]

        self.dtypes = {
            'MSG_TYPE': str,
            'NODE_1': str,
            'NODE_2': str,
            'SEQTS': str,
            'HLC': float,
            'BITMAP': str,
            'OFFSETS': str,
            'COUNTERS': float,
            'NUM_PROCS': float,
            'EPSILON': float,
            'INTERVAL': float,
            'DELTA': float,
            'ALPHA': float,
            'MAX_OFFSET_SIZE': float,
            'OFFSET_SIZE': float,
            'COUNTER_SIZE': float,
            'CLOCK_SIZE': float,
            'MAX_OFFSET': float,
            'MSG_BODY': str
        }

    def convert_df_to_list(self, df: pd.DataFrame):

        event_list = []
        event_uid = 0

        for index, row in df.iterrows():

            if index == 0:
                continue
            
            e = Event(
                event_id=event_uid,
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
            event_uid += 1

        return event_list
    
    def parse_contents(self, contents, filename, date):
        content_type, content_string = contents.split(',')

        decoded = base64.b64decode(content_string)
        df = pd.read_csv(
            io.StringIO(decoded.decode('utf-8')), 
            dtype=str, 
            low_memory=False, 
            header=None
        )
        
        return df

    def process_file(self, list_of_contents, list_of_names, list_of_dates):

        df = self.parse_contents(list_of_contents, list_of_names, list_of_dates)

        df.columns = self.columns

        events = self.convert_df_to_list(df)

        return events
    
    def process_csv(self, filename):

        df = pd.read_csv(
            filepath_or_buffer=filename,
            dtype=str, 
            low_memory=False, 
            header=None
        )

        df.columns = self.columns

        events = self.convert_df_to_list(df)

        return events