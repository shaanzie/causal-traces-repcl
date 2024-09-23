import argparse
from dash import Dash, html, dcc, Output, Input, callback, State
import plotly.graph_objects as go
import json
from configparser import ConfigParser

import processor
import processor.csv_processor
import processor.json_processor
import processor.processor
from schedule.candidate_traces import CandidateTraces
from tracer.tracer import Tracer
from tracer.new_tracer import NewTracer
from schedule.schedule_tree import Forest

from graphers.replayer import Replayer

from exporter.exporter import Exporter

# External stylesheet link
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Holds the event list
events = []

def generate_cfgdata(filename: str):

    parser = ConfigParser()
    parser.read(filenames=filename)

    cfg = dict(parser.items('generic'))

    cfg['nodes'] = cfg['nodes'].split(',')

    return cfg

# Argument parser
parser = argparse.ArgumentParser(
    prog="RepViz Graphical Interface Server"
)

parser.add_argument('-cfg', '--config', help='Configuration file')

args = parser.parse_args()

cfg = generate_cfgdata(args.config)

if(cfg['csv'] != '0'):
    events = processor.csv_processor.CSVProcessor(cfg).process_csv(cfg['data'])
else:
    events = processor.json_processor.JSONProcessor(cfg).process_dir(cfg['data'])
    
# print(events)

# schedule = Forest()
schedule = CandidateTraces()

# schedule_tree = schedule.build_schedule_tree(grouped_events)

# schedule.build_candidate_traces(schedule_tree)

# schedule.generate_candidate_traces(events, int(cfg['cwnd']))

for cwnd in range(0, 21):
    schedule.generate_candidate_traces(events, cwnd/10)

# Now we play the replay on the UNIX interface

# tracer = Tracer()
# tracer = NewTracer()

# grouped_events = tracer.order_events(events)

# tracer.run_new_replay(events)
# tracer.run_replay(events)

# Replayable Graph

f = open('generated_trace.json')
trace = json.load(f)
f.close()

exporter = Exporter()
exporter.convert_trace_to_lc(trace=trace['trace'])

f = open(r'generated_trace.json', 'w')
f.write(json.dumps(trace))
    
swimlane_grapher = Replayer(cfg, go.Figure())
swimlane_grapher.generate_base_figure()

f = open('candidate_traces.json')
candidate_traces = json.load(f)

candidate_grapher = Replayer(cfg, go.Figure())
candidate_grapher.generate_base_figure()

options = list(range(0, len(candidate_traces["candidate_traces"])))

process_grapher = Replayer(cfg, go.Figure())
process_grapher.generate_base_figure()

process_options = cfg["nodes"]

# Helper function to generate blank figures
def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template=None)
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)
    return fig

# Initialize app
app = Dash(external_stylesheets=external_stylesheets)

# Define app layout
app.layout = [

    html.Div(children='RepViz Graphical Interface'),
    html.Div(id='swimlane-graph-objects', children=[
        html.Button('Replay Event', id='replay-button', n_clicks=0),
        dcc.ConfirmDialog(id='confirm', message='No more events to replay'),
        dcc.Graph(figure=swimlane_grapher.get_figure(), id='swimlane', style={'width': '100%', 'height': '90vh'}, animate=False, clear_on_unhover=True),
        html.Div(id='user-log')
    ]),
    html.Div(id='candidate-graph-holder', children=[
        dcc.Dropdown(options=options, placeholder="Select a trace", id="trace-selector"),
        html.Button('Replay Candidate Trace Event', id='candidate-replay-button', n_clicks=0),
        html.Button('Reset Graph', id='candidate-reset-button', n_clicks=0),
        dcc.ConfirmDialog(id='candidate-confirm', message='No more events to replay'),
        dcc.Graph(figure=candidate_grapher.get_figure(), id='candidate', style={'width': '100%', 'height': '90vh'}, animate=False),
        html.Div(id='candidate-log'),
    ]),
    html.Div(id='process-graph-holder', children=[
        dcc.Dropdown(options=options, placeholder="Select a trace", id="process-trace-selector"),
        dcc.Dropdown(options=process_options, placeholder="Select a process", id="process-selector"),
        html.Button('Replay Process Event', id='process-replay-button', n_clicks=0),
        html.Button('Reset Graph', id='process-reset-button', n_clicks=0),
        dcc.ConfirmDialog(id='process-confirm', message='No more events to replay'),
        dcc.Graph(figure=process_grapher.get_figure(), id='process', style={'width': '100%', 'height': '90vh'}, animate=False),
        html.Div(id='process-log'),
    ]),
]

# Iterator for event list
event_list_iterator = 0
@callback(
    Output('swimlane', 'figure'),
    Output('user-log', 'children'),
    Output('confirm', 'displayed'),
    Input('replay-button', 'n_clicks'),
    prevent_initial_call=True
)
def add_next_event(n_clicks: int):

    global event_list_iterator

    if event_list_iterator >= len(trace['trace']):
        return swimlane_grapher.get_figure(), [], 1

    event = trace['trace'][event_list_iterator]

    dialog = 0

    if n_clicks > 0:
        swimlane_grapher.add_event(event=event, json_trace=trace)
        div = html.Div(children='{}'.format(event))
        event_list_iterator += 1

    return swimlane_grapher.get_figure(), [div], dialog

# Iterator for event list
candidate_list_iterator = 0
@callback(
    Output('candidate', 'figure'),
    Output('candidate-log', 'children'),
    Output('candidate-confirm', 'displayed'),
    Input('candidate-replay-button', 'n_clicks'),
    Input('trace-selector', 'value'),
    prevent_initial_call=True
)
def update_candidate_figure(n_clicks, value):

    global candidate_list_iterator

    trace = candidate_traces["candidate_traces"][value]

    if candidate_list_iterator >= len(trace['trace']):
        return candidate_grapher.get_figure(), [], 1

    event = trace['trace'][candidate_list_iterator]

    dialog = 0

    if n_clicks > 0:
        candidate_grapher.add_event(event=event, json_trace=trace)
        div = html.Div(children='{}'.format(event))
        candidate_list_iterator += 1

    return candidate_grapher.get_figure(), [div], dialog


# Iterator for event list
process_list_iterator = 0
@callback(
    Output('process', 'figure'),
    Output('process-log', 'children'),
    [
        Input('process-replay-button', 'n_clicks'),
        Input('process-trace-selector', 'value'),
        Input('process-selector', 'value'),
    ],
    prevent_initial_call=True
)
def update_process_figure(n_clicks, value, process):

    global process_list_iterator

    trace = candidate_traces["candidate_traces"][value]['trace']
    print(value, process)
    print(trace)

    process_trace = {
        "trace": []
    }
    for event in trace:
        try:
            print(event)
            if event['node_1'] == process or event['node_2'] == process:
                process_trace['trace'].append(event)
        except Exception as e:
            print(e)

    print(process_trace)

    event = process_trace['trace'][process_list_iterator]

    if n_clicks > 0:
        process_grapher.add_event(event=event, json_trace=process_trace)
        div = html.Div(children='{}'.format(event))
        process_list_iterator += 1

    return process_grapher.get_figure(), [div]

if __name__ == '__main__':

    app.run_server()