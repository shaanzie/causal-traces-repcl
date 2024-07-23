import json
import plotly.graph_objects as go
from event.event import Event

class Replayer:

    def __init__(self, meta: dict, fig: go.Figure) -> None:
        self.meta = meta
        self.fig = fig

    def get_figure(self):
        return self.fig

    def generate_base_figure(self):

        self.fig = go.Figure()
        self.fig.update_xaxes(range=[0, self.meta['xlim']])
        self.fig.update_yaxes(range=[0, self.meta['num_procs'] + 1])

        self.fig.update_layout(
            yaxis = dict(
                tickmode = 'array',
                tickvals = [i for i in range(1, len(self.meta['nodes']) + 1)],
                ticktext = self.meta['nodes']
            )
        )

        for proc in range(self.meta['num_procs']):
            
            self.fig.add_shape(
                type="line",
                x0=0,
                y0=proc + 1,
                x1=self.meta['xlim'],
                y1=proc + 1,
                line_width=0.5,
            )

        return self.fig

    def add_event(self, event: Event, json_trace: dict):

        print('Replaying {}'.format(event))
        
        proc = self.meta[event['node_1']]

        x0=event['event_time']['hlc'] - 0.3
        y0=proc - 0.3
        x1=event['event_time']['hlc'] + 0.3
        y1=proc + 0.3

        if event['event_type'] == "SEND":
            color = 'LightSeaGreen'
        else:
            color = 'rosybrown'

        self.fig.add_shape(
            type='circle',
            xref='x',
            yref='y',
            x0=x0,
            y0=y0,
            x1=x1,
            y1=y1,
            fillcolor=color
        )
        
        self.fig.add_trace(go.Scatter(
            x=[event['event_time']['hlc']],
            y=[proc],
            mode='markers',
            marker=dict(size=20, color='rgba(0,0,0,0)'),
            hoverinfo='text',
            text='{}'.format(event['msg_body']),
        ))

        if(event["event_type"] == "RECV"):
            self.add_event_arrow(event=event, json_trace=json_trace)

    def add_event_arrow(self, event: Event, json_trace: dict):

        send_time = 0

        for e in json_trace["trace"]:
            if(e["seqts"] == event["seqts"] and e["event_type"] == 'SEND' and e["node_2"] == event["node_1"] and e["node_1"] == event["node_2"]):
                send_time = e["event_time"]["hlc"]

        proc_1 = self.meta[event["node_2"]] 
        proc_2 = self.meta[event["node_1"]] 
        x0 = send_time
        x1 = event["event_time"]["hlc"]
        y0 = proc_1
        y1 = proc_2

        self.fig.add_shape(
            type="line",
            x0=x0, y0=y0, x1=x1, y1=y1,
            line=dict(
                color="RoyalBlue",
                width=1
            ),
            # Add arrowhead
            xref="x", yref="y"
        )
        self.fig.add_annotation(
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
            arrowsize=3,
            arrowwidth=1,
            arrowcolor="RoyalBlue"
        )