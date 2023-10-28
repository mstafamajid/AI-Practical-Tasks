from flask import Flask, render_template
import math
import heapq
import time

app = Flask(__name__)

solutionEdgeId = 0
def getId():
    global solutionEdgeId
    newId = solutionEdgeId
    solutionEdgeId += 1
    return newId


class TreeNode:
    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

class Tree:
    def __init__(self):
        self.root = None

    def add_node(self, parent_name, name, data):
        new_node = TreeNode(name, data)
        if not self.root:
            # If the tree is empty, set the new node as the root
            self.root = new_node
        else:
            # Find the parent node by name and add the new node as its child
            parent_node = self.find_node_by_name(parent_name, self.root)
            if parent_node:
                parent_node.add_child(new_node)
            else:
                print(f"Parent node with name '{parent_name}' not found. Node not added.")

    def find_node_by_name(self, name, current_node):
        if current_node.name[1:-1] == name[1:-1]:
            return current_node
        for child in current_node.children:
            result = self.find_node_by_name(name, child)
            if result:
                return result
        return None

    
    
    

    def to_dict(self, node=None):
        if node is None:
            node = self.root

        tree_dict = {
            'label': node.name,
            'name': node.name,
        }

        if node.children:
            tree_dict['children'] = [self.to_dict(child) for child in node.children]

        return tree_dict



def a_star(nodes, start, goal):
    priority_queue = [(0, start)]  # Priority queue with (total cost, node)
    visited = set()
    parent = {}  # Parent dictionary for backtracking
    g_score = {node: float('inf') for node in nodes}
    g_score[start] = 0
    tree = Tree()
    step=0
    tree.add_node(None, f"{str(step)} {start}-0-{nodes[start]['cost']}-{nodes[start]['cost']}", "")

    while priority_queue:
        total_cost, current_node = heapq.heappop(priority_queue) # total , current_node  name
        if current_node == goal:
            # Backtrack to find the best path
            path = []
            while current_node in parent:
                path.insert(0, current_node + " " + str(g_score[current_node]) + "-" + str(nodes[current_node]['cost']) + "-" + str(nodes[current_node]['cost'] + g_score[current_node]))
                current_node = parent[current_node]
            path.insert(0, start+" 0-"+ str(nodes[current_node]['cost'])+ "-" + str(nodes[current_node]['cost']))
            
           
            return path,tree

        if current_node in visited:
            continue

        visited.add(current_node)

        for neighbor, edge_cost in get_neighbors(current_node):
            tentative_g_score = g_score[current_node] + edge_cost
            tree.add_node(f"{str(step)} {current_node}-{g_score[current_node]}-{nodes[current_node]['cost']}-{nodes[current_node]['cost']+g_score[current_node]}", f"{str((step+1))} {neighbor}-{tentative_g_score}-{nodes[neighbor]['cost']}-{nodes[neighbor]['cost']+tentative_g_score}", "")
            step=step+1
            if tentative_g_score < g_score[neighbor]:
                parent[neighbor] = current_node
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + euclidean_distance(nodes[neighbor], nodes[goal])
                heapq.heappush(priority_queue, (f_score, neighbor))

    return None  # No path found

def get_neighbors(node):
    # Return a list of neighbors and their costs from the current node
    # Implement your logic to determine neighbors based on edges
    # For example, based on your existing 'edges' dictionary
    neighbors = []
    for edge, cost in edges.items():
        if edge.startswith(node + '-'):
            neighbor = edge.split('-')[1]
            neighbors.append((neighbor, cost))
    return neighbors


def euclidean_distance(node1, node2):
    row1, col1 = node1["row"], node1["col"]
    row2, col2 = node2["row"], node2["col"]
    return round(math.sqrt((row1 - row2) ** 2 + (col1 - col2) ** 2), 1)


@app.route("/", methods=["GET"])
def index():
    nodes = {
        "s": {"row": 0, "col": 2, "cost": 99},
        "a": {"row": 2, "col": 0, "cost": 99},
        "b": {"row": 2, "col": 1, "cost": 99},
        "c": {"row": 2, "col": 3, "cost": 99},
        "e": {"row": 4, "col": 1, "cost": 99},
        "d": {"row": 4, "col": 2, "cost": 99},
        "f": {"row": 5, "col": 2, "cost": 99},
        "g": {"row": 6, "col": 0, "cost": 99},
    }

    global edges
    edges = {
        "s-a": 6,
        "s-b": 5,
        "s-c": 10,
        "a-e": 6,
        "b-e": 6,
        "b-d": 7,
        "c-d": 6,
        "e-f": 4,
        "d-f": 6,
        "f-g": 3
    }

    # start and end
    start = "s"
    goal = "g"

    for node_name, node_info in nodes.items():
        distance = euclidean_distance(node_info, nodes[goal])
        node_info['cost'] = distance
    
    
    bestPath,tree = a_star(nodes, start, goal)

    solutionEdges = tree.to_dict()

    
    return render_template("index.html", nodes=nodes, edges=edges, solutionEdges=solutionEdges, bestPath=bestPath)



if __name__ == "__main__":
    app.run(debug=True)
