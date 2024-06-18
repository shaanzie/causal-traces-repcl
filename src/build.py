from flask import Flask, request, jsonify
from dash import Dash, html, dcc, Output, Input, callback
import json
from matplotlib import figure
import plotly.express as px
import plotly.graph_objects as go
import argparse
import pandas as pd

from event.event import Event
from replay_clock.replay_clock import ReplayClock

from tracer.tracer import Tracer
from schedule.schedule_tree import FamilyOfSchedules

from graphers.swimlane import Swimlane
from graphers.tree import TreeGrapher

def get_metadata(trace):

    num_procs = len(trace["trace"][0]["event_time"]["offsets"])
    xlim = (trace["trace"][-1]["event_time"]["hlc"])*2
    
    meta = {
        'num_procs': num_procs,
        'xlim': xlim,
    }

    for i in range(num_procs):
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
            receiver=row['NODE_2']
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
        'MAX_OFFSET'
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
        'MAX_OFFSET': float
    }

    df = pd.read_csv(
        filepath_or_buffer=args.filename,
        dtype=str, 
        low_memory=False, 
        header=None
    )

    df.columns = columns

    events = convert_df_to_list(df)

    # send_init_params_to_server(df)

    tracer = Tracer(events)

    grouped_events = tracer.order_events()

    schedule = FamilyOfSchedules()

    schedule_tree = schedule.build_schedule_tree(grouped_events)

    schedule.printAllRootToLeafPaths(schedule_tree)

    tracer.run_replay(grouped_events)

    f = open('generated_trace.json')
    json_trace = json.load(f)

    meta = get_metadata(json_trace)

    swimlane_grapher = Swimlane(meta, go.Figure())
    swimlane_fig = swimlane_grapher.generate_graph(json_trace=json_trace)

    tree_grapher = TreeGrapher(meta, go.Figure())
    tree_fig = tree_grapher.generate_graph(json_trace=json_trace)

    app = Dash()

    app.layout = [

        html.Div(children='RepViz Graphical Interface'),
        dcc.Graph(figure=swimlane_fig, id='swimlane', style={'width': '100%', 'height': '90vh'}, animate=False),
        dcc.Graph(figure=tree_fig, id='tree', style={'width': '100%', 'height': '90vh'}, animate=False)

    ]

    app.run_server()