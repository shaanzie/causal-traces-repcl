import json
import os

from processor.processor import FileProcessor

from event.event import Event
from replay_clock.replay_clock import ReplayClock

class JSONProcessor(FileProcessor):

    def __init__(self, cfg: dict) -> None:
        
        super().__init__(cfg)
        # print(cfg)

    def convert_raw_to_list(self, raw_events: dict):

        events = {}

        for node in raw_events.keys():

            events[node] = []

            for event in raw_events[node]['events']:

                e = Event(
                    event_id    =   int(event['event_id']),
                    seqts       =   event['seqts'],
                    event_type  =   event['event_type'],
                    event_time  =   ReplayClock(
                            nodeId      =   event['nodeId'],
                            hlc         =   int(event['hlc']),
                            bitmap      =   event['bitmap'],
                            offsets     =   event['offsets'],
                            counters    =   int(event['counters']),
                            offset_size =   int(event['offset_size']),
                            epsilon     =   int(event['epsilon'])
                    ),
                    sender      =   event['sender'],
                    receiver    =   event['receiver'],
                    msg_body    =   event['msg_body']
                )
            
                events[node].append(e)
        
        return events

    
    def process_dir(self, directory_path):

        raw_events = {}

        # Iterate over the files in the specified directory
        for filename in os.listdir(directory_path):
            # Check if the file is a JSON file
            if filename.endswith('.json'):
                file_path = os.path.join(directory_path, filename)
                
                # Open and read the JSON file
                with open(file_path, 'r') as file:
                    try:
                        # Parse the JSON content and add it to the dictionary
                        data = json.load(file)
                        raw_events[filename.split('.')[0]] = data
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON from file {filename}: {e}")

        events = self.convert_raw_to_list(raw_events)

        return events