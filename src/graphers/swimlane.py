import json
import plotly.graph_objects as go
from event.event import Event

class Swimlane:

    def __init__(self, meta: dict, fig: go.Figure) -> None:
        self.meta = meta
        self.fig = fig

    def get_figure(self) -> go.Figure:
        return self.fig

    def generate_base_figure(self):

        self.fig = go.Figure()
        self.fig.update_xaxes(range=[-500, self.meta['xlim']])
        self.fig.update_yaxes(range=[0, 500 * self.meta['num_procs']])

        self.fig.layout.yaxis.showticklabels = False

        for proc in range(self.meta['num_procs']):
            self.fig.add_shape(
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
            self.fig.add_shape(
                type="line",
                x0=0,
                y0=500*proc + 225,
                x1=self.meta['xlim'],
                y1=500*proc + 225,
                line_width=0.5,
            )


    def add_events(self, json_trace: dict) -> None:

        for event in json_trace["trace"]:

            self.add_event(event)
            
            if(event["event_type"] == "RECV"):
                self.add_event_arrow(event, json_trace)


    def add_event(self, event: Event) -> None:

        proc = self.meta[event['node_1']] - 1
        
        x0=event['event_time']['hlc'] - 5
        y0=500*proc + 230
        x1=event['event_time']['hlc'] + 5
        y1=500*proc + 220

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
            x=[(x0 + x1) / 2],
            y=[(y0 + y1) / 2],
            mode='markers',
            marker=dict(size=20, color='rgba(0,0,0,0)'),
            hoverinfo='text',
            text='{}'.format(event['msg_body']),
        ))


    def add_event_arrow(self, event: Event, json_trace: dict) -> None:

        send_time = 0

        for e in json_trace["trace"]:
            if(e["seqts"] == event["seqts"] and e["event_type"] == 'SEND' and e["node_2"] == event["node_1"] and e["node_1"] == event["node_2"]):
                send_time = e["event_time"]["hlc"]

        proc_1 = self.meta[event["node_2"]] - 1
        proc_2 = self.meta[event["node_1"]] - 1
        x0 = send_time
        x1 = event["event_time"]["hlc"]
        y0 = 500*proc_1 + 225
        y1 = 500*proc_2 + 225

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

    def generate_graph(self, json_trace: dict) -> go.Figure:
        
        self.generate_base_figure()

        self.add_events(json_trace)

        return self.get_figure()