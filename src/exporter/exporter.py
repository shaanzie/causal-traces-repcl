from datetime import datetime
import time 

current_logical_maxt = 0
current_pt_maxt = 0

class Exporter:

    def __init__(self) -> None:
        pass

    def convert_trace_to_lc(self, trace: list):
        
        global current_logical_maxt
        
        current_logical_maxt = 0

        for event in trace:
            current_logical_maxt += 1
            event['logical_time'] = current_logical_maxt
    
    def convert_trace_to_pt(self, trace: list, granularity: int):
        
        global current_pt_maxt

        for event in trace:
            current_pt_maxt = max(current_pt_maxt, event['event_time']['hlc']) + granularity
            current_pt_maxt += event['event_time']['counters'] / granularity
            event['physical_time'] = datetime.fromtimestamp(current_pt_maxt)