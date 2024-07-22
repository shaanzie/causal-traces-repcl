import sched
from dash import Dash, html, dcc, Output, Input, callback
import json
import plotly.express as px
import plotly.graph_objects as go
import argparse
import pandas as pd

from event.event import Event
from replay_clock.replay_clock import ReplayClock

from tracer.tracer import Tracer
from schedule.schedule_tree import FamilyOfSchedules

from graphers.swimlane import Swimlane
from graphers.candidates import CandidateGraph

def get_metadata(trace):

    num_procs = len(trace["trace"][0]["event_time"]["offsets"])
    xlim = (trace["trace"][-1]["event_time"]["hlc"]) + 500
    
    meta = {
        'num_procs': num_procs,
        'xlim': xlim,
        'nodes': []
    }

    for i in range(num_procs):
        meta['nodes'].append("10.1.1.{}".format(i + 1))
        meta["10.1.1.{}".format(i + 1)] = i + 1

    print(meta)

    return meta

def convert_df_to_list(df: pd.DataFrame):

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




if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog="RepViz Graphical Interface"
    )

    parser.add_argument('filename', help='Input the file to be graphed')
    args = parser.parse_args()

    columns = [
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

    dtypes = {
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

    df = pd.read_csv(
        filepath_or_buffer=args.filename,
        dtype=str, 
        low_memory=False, 
        header=None
    )

    df.columns = columns

    events = convert_df_to_list(df)

    tracer = Tracer()

    grouped_events = tracer.order_events(events)

    schedule = FamilyOfSchedules()

    schedule_tree = schedule.build_schedule_tree(grouped_events)

    schedule.build_candidate_traces(schedule_tree)

    tracer.run_new_replay(events)

    f = open('generated_trace.json')
    json_trace = json.load(f)

    meta = get_metadata(json_trace)

    swimlane_grapher = Swimlane(meta, go.Figure())
    swimlane_fig = swimlane_grapher.generate_graph(json_trace=json_trace)

    f.close()
    f = open('candidate_traces.json')
    candidate_traces = json.load(f)
    
    candidate_grapher = CandidateGraph(meta, go.Figure(), candidate_traces=candidate_traces)
    candidate_fig = candidate_grapher.fig

    process_fig = go.Figure()

    options = list(range(0, len(candidate_traces["candidate_traces"])))
    process = meta["nodes"]

    app = Dash()

    app.layout = [

        html.Div(children='RepViz Graphical Interface'),
        dcc.Graph(figure=swimlane_fig, id='swimlane', style={'width': '100%', 'height': '90vh'}, animate=False, clear_on_unhover=True),
        dcc.Tooltip(id='swimlane-tooltip'),
        dcc.Dropdown(options=options, placeholder="Select a trace", id="trace-selector"),
        dcc.Dropdown(options=process, placeholder="Select a process", id="process-selector"),
        html.Div(id='graph-holder', children=[
            dcc.Graph(figure=candidate_fig, id='candidate', style={'width': '100%', 'height': '90vh'}, animate=False),
            dcc.Graph(figure=process_fig, id='process', style={'width': '100%', 'height': '90vh'}, animate=False),
        ]),
        html.Div(id='trace-log'),


    ]

    @callback(
        Output('candidate', 'figure'),
        Output('trace-log', 'children'),
        Input('trace-selector', 'value')
    )
    def update_candidate_figure(value):
    
        candidate_fig = candidate_grapher.generate_graph(value=value)

        div_list = []
        candidate_trace = schedule.get_trace(value=value)
        for event in candidate_trace:
            div = html.Div(children='{}'.format(event))
            div_list.append(div)
    
        return candidate_fig, div_list
        
    
    @callback(
        Output('process', 'figure'),
        Input('trace-selector', 'value'),
        Input('process-selector', 'value')
    )
    def update_process_figure(trace, process):

        candidate_trace = schedule.get_trace(value=trace)
        process_trace = {
            "trace": []
        }
        for event in candidate_trace:
            try:
                if event.sender == process or event.receiver == process:
                    process_trace['trace'].append(event.jsonify())
            except Exception as e:
                print(e)

        swimlane = Swimlane(meta, go.Figure())

        swimlane.generate_graph(process_trace)

        return swimlane.get_figure()
    

    app.run_server()