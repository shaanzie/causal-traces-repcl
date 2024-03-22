from tracer.tracer import Tracer
from event.event import Event
from replay_clock.replay_clock import ReplayClock
import pandas as pd

def convert_df_to_list(df: pd.DataFrame):

    event_list = []

    for index, row in df.iterrows():
        if index == 0:
            continue
        
        e = Event(
            event_id=0,
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
            receiver=row['NODE_2']
        )
        event_list.append(e)

    return event_list

if __name__ == '__main__':

    columns = [
        'MSG_TYPE',
        'NODE_1',
        'NODE_2',
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
        'MAX_OFFSET'
    ]

    dtypes = {
        'MSG_TYPE': str,
        'NODE_1': str,
        'NODE_2': str,
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
        'MAX_OFFSET': float
    }

    df = pd.read_csv(
        filepath_or_buffer='/Users/ishaanlagwankar/Desktop/code/causal-traces-repcl/sample_trace.csv',
        dtype=str, 
        low_memory=False, 
        header=None
    )

    df.columns = columns

    events = convert_df_to_list(df)

    tracer = Tracer(events)

    grouped_events = tracer.order_events()