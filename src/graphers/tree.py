import plotly.graph_objects as go
from schedule.schedule_tree import FamilyOfSchedules
from tracer.tracer import Tracer

class TreeGrapher:

    def __init__(self, meta: dict, fig: go.Figure) -> None:
        self.meta = meta
        self.fig = fig

    def generate_graph(self, json_trace: dict) -> go.Figure:
        return self.fig