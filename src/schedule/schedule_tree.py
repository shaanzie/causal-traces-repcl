class TreeNode:
    
    def __init__(self, nodeId, event):
        self.nodeId = nodeId
        self.event = event
        self.children = []
        
    def __repr__(self):
        return 'EventId={}, children={}'.format(self.event_id, self.children)
    
    def add_child(self, node: 'TreeNode'):
        self.children.append(node)

class FamilyOfSchedules:

    def __init__(self) -> None:
        self.vec = []

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

        for ele in self.vec:
            print(ele, end = " ")
            
        print()
    
    def printAllRootToLeafPaths(self, root):
        
        if (not root):
            return

        self.vec.append(root.nodeId)
    
        if (len(root.children) == 0):

            self.printPath()
            self.vec.pop()
            return
    
        # Recur for all children of
        # the current node
        for i in range(len(root.children)):
    
            # Recursive Function Call
            self.printAllRootToLeafPaths(root.children[i])
            
        self.vec.pop()    
    
    # Function to print root to leaf path
    def printRootToLeafPaths(self, root):
        
        if (not root):
            return
        
        self.printAllRootToLeafPaths(root)