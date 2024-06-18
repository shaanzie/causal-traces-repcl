from flask import Flask, request, jsonify
from dash import Dash, html, dcc, Output, Input, callback
import json
from matplotlib import figure
import plotly.express as px
import plotly.graph_objects as go
import argparse

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

def generate_base_figure(meta):

    fig = go.Figure()
    fig.update_xaxes(range=[-500, meta['xlim']])
    fig.update_yaxes(range=[0, 500*meta['num_procs']])

    fig.layout.yaxis.showticklabels = False

    for proc in range(meta['num_procs']):
        fig.add_shape(
            type='rect',
            xref='x',
            yref='y',
            x0=-500,
            y0=500*proc + 50,
            x1=0,
            y1=500*(proc + 1),
            fillcolor='LightSkyBlue',
            label=dict(text="10.1.1.{}".format(proc + 1))
        )
        fig.add_shape(
            type="line",
            x0=0,
            y0=500*proc + 225,
            x1=meta['xlim'],
            y1=500*proc + 225,
            line_width=0.5,
        )


    return fig


def add_events(fig, json_trace, meta):

    for event in json_trace["trace"]:

        fig = add_event(event, fig)
        
        if(event["event_type"] == "RECV"):
            fig = add_event_arrow(event, fig, meta)

    return fig


def add_event(event, fig):

    proc = meta[event['node_1']] - 1
    
    x0=event['event_time']['hlc'] - 5
    y0=500*proc + 230
    x1=event['event_time']['hlc'] + 5
    y1=500*proc + 220

    if event['event_type'] == "SEND":
        color = 'LightSeaGreen'
    else:
        color = 'rosybrown'

    fig.add_shape(
        type='circle',
        xref='x',
        yref='y',
        x0=x0,
        y0=y0,
        x1=x1,
        y1=y1,
        fillcolor=color
    )

    return fig


def add_event_arrow(event, fig, meta):

    send_time = 0

    for e in json_trace["trace"]:
        if(e["event_id"] == event["event_id"] and e["event_type"] == 'SEND' and e["node_2"] == event["node_1"] and e["node_1"] == event["node_2"]):
            send_time = e["event_time"]["hlc"]

    proc_1 = meta[event["node_2"]] - 1
    proc_2 = meta[event["node_1"]] - 1
    x0 = send_time
    x1 = event["event_time"]["hlc"]
    y0 = 500*proc_1 + 225
    y1 = 500*proc_2 + 225

    fig.add_shape(
        type="line",
        x0=x0, y0=y0, x1=x1, y1=y1,
        line=dict(
            color="RoyalBlue",
            width=1
        ),
        # Add arrowhead
        xref="x", yref="y"
    )
    fig.add_annotation(
        x=x1,
        y=y1,
        ax=x0,
        ay=y0,
        xref="x",
        yref="y",
        axref="x",
        ayref="y",
        showarrow=True,
        arrowhead=1,
        arrowsize=1,
        arrowwidth=1,
        arrowcolor="RoyalBlue"
    )

    return fig

parser = argparse.ArgumentParser(
    prog="RepViz Graphical Interface"
)

parser.add_argument('filename', help='Input the file to be graphed')
args = parser.parse_args()

f = open(args.filename)
json_trace = json.load(f)

meta = get_metadata(json_trace)

fig = generate_base_figure(meta)

fig = add_events(fig, json_trace, meta)

app = Dash()

app.layout = [

    html.Div(children='RepViz Graphical Interface'),
    dcc.Graph(figure=fig, id='swimlane', style={'width': '100%', 'height': '90vh'}, animate=True)

]


if __name__ == "__main__":

    app.run_server(debug=True)