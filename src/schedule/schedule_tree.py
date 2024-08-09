from copy import deepcopy
import json


class TreeNode:
    
    def __init__(self, nodeId, event):
        self.nodeId = nodeId
        self.event = event
        self.children = []
        
    def __str__(self, level=0):
        ret = "\t"*level+repr(self.nodeId)+"\n"
        for child in self.children:
            ret += child.__str__(level+1)
        return ret

    def __repr__(self):
        return '<tree node representation>'
    
    def add_child(self, node: 'TreeNode'):
        self.children.append(node)

class Forest:

    def __init__(self) -> None:
        self.vec = []
        self.candidate_traces = []

    def lr(self, arr):
        temp = arr[0]
        for i in range(len(arr)-1):
            arr[i] = arr[i+1]
        arr[len(arr)-1] = temp

    def add_mini_tree(self, events):
        head = TreeNode(events[0].event_id, events[0])
        temp = head
        for i in range(len(events)):
            if i == 0:
                pass
            else:
                newnode = TreeNode(events[i].event_id, events[i])
                temp.add_child(newnode)
                temp = newnode
        return head, temp
    
    def build_schedule_tree(self, event_list):
        
        head = TreeNode(0, 0)
        temp = head
        tails = []
        for events in event_list:
            if len(events) == 1:
                newnode = TreeNode(events[0].event_id, events[0])
                temp.add_child(newnode)
                temp = newnode
            else:
                for i in range(len(events)):
                    newnode, tail = self.add_mini_tree(events)
                    temp.add_child(newnode)
                    tails.append(tail)
                    self.lr(events)
                dead_tail = TreeNode(-1, -1)
                for j in range(0, len(tails)):
                    tails[j].add_child(dead_tail)
                temp = dead_tail
                tails = []
        
        return head
    
    def printPath(self):

        candidate_trace = deepcopy(self.vec)
        self.candidate_traces.append(candidate_trace)
    
    def printAllRootToLeafPaths(self, root):
        
        if (not root):
            return

        self.vec.append(root.event)
    
        if (len(root.children) == 0):

            self.printPath()
            self.vec.pop()
            return
    
        for i in range(len(root.children)):
    
            self.printAllRootToLeafPaths(root.children[i])
            
        self.vec.pop()    
        
    def printRootToLeafPaths(self, root):
        
        if (not root):
            return
        
        self.printAllRootToLeafPaths(root)

    def build_candidate_traces(self, schedule_tree: TreeNode):

        self.printRootToLeafPaths(schedule_tree)

        json_trace = dict()
        json_trace['candidate_traces'] = []

        for trace in range(len(self.candidate_traces)):
            
            json_trace['candidate_traces'].insert(trace, {'trace_id': trace})
            json_trace['candidate_traces'][trace]['trace'] = []
            for event in self.candidate_traces[trace]:
                    try:
                        json_trace['candidate_traces'][trace]['trace'].append(event.jsonify())
                    except:
                        pass
        
        Trace_File = open(r'candidate_traces.json', 'w')
        Trace_File.write(json.dumps(json_trace))

    def get_trace(self, value: int):
        return self.candidate_traces[value]