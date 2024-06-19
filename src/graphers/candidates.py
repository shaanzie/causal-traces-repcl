from copy import deepcopy
import plotly.graph_objects as go
from schedule.schedule_tree import FamilyOfSchedules
from tracer.tracer import Tracer
from schedule.schedule_tree import TreeNode
from graphers.swimlane import Swimlane

class CandidateGraph:

    def __init__(self, meta: dict, fig: go.Figure, candidate_traces: dict) -> None:
        self.meta = meta
        self.fig = fig
        self.vec = []
        self.candidate_traces = candidate_traces


    def add_to_graph(self, node: TreeNode, idx: int):
        
        x0 = 4 * idx
        x1 = 4 * idx + 2
        y0 = 0
        y1 = 2
        color = 'LightSeaGreen'

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
    
    def add_arrow(self, node1: TreeNode, node2: TreeNode):
        pass

    def generate_graph(self, value: int):
        
        # Drawing for Trace value

        trace = self.candidate_traces["candidate_traces"][value]

        swimlane = Swimlane(self.meta, go.Figure())

        swimlane.generate_graph(trace)

        return swimlane.get_figure()