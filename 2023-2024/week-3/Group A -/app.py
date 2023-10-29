import json
from queue import PriorityQueue
from flask import Flask, render_template


app = Flask(__name__)



def manhatn_destance(node1, node2):

    return abs(node1['row']-node2['row'])+abs(node1['col']-node2['col'])

# Define the A* algorithm function

def astar_search(start, goal, nodes, edges):
    open_set = PriorityQueue()
    open_set.put((nodes[start]["cost"], start))
    came_from = {}
    g_score = {node: float('inf') for node in nodes}
    g_score[start] = 0

    # Initialize the solution tree with the start node
    solution_tree = {
            "label": f"{start}-{g_score[start]}-{nodes[start]['cost']}-{g_score[start] + nodes[start]['cost']}",
            "children": []
        
    }

    while not open_set.empty():
        _, current = open_set.get()
        
       
        if current == goal:
            path = [] #[s,b,e,f,g]
            while current in came_from:
                path.insert(0, current)
                current = came_from[current]
            return path, solution_tree  # Return both the path and the solution tree

        for neighbor in nodes:
            if neighbor == 's':
                continue

            key = "-".join([current, neighbor]) 
            tentative_g_score = g_score[current] + edges.get((key), float('inf'))
           

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current  
                g_score[neighbor] = tentative_g_score
                f_score = g_score[neighbor] + manhatn_destance(nodes[neighbor], nodes[goal])

                open_set.put((f_score, neighbor))
                
               
                
                
            if g_score[neighbor]!=float('inf') and tentative_g_score != float('inf'):

                 
                 neighbor_node = {
                    "id": 0,
                    "label": f"{neighbor}-{g_score[neighbor]}-{nodes[neighbor]['cost']}-{g_score[neighbor] + manhatn_destance(nodes[neighbor], nodes[goal])}",
                    "children": []
                }
                 targe=f"{current}-{g_score[current]}-{nodes[current]['cost']}-{g_score[current] + manhatn_destance(nodes[current], nodes[goal])}"
                 parent_node = find_node(solution_tree, targe)
                
                 parent_node["children"].append(neighbor_node)


    return None, None  # Return None if no path is found
def find_node(node, target_label):
    print(target_label)
    print("hello")
    print(node["label"])
    if target_label == node["label"]:
            return node
    for child in node.get("children", []):
            found_node = find_node(child, target_label)
            if found_node:
                return found_node
    return None
# Example usage:



@app.route("/", methods=["GET"])
def index():

    nodes = {
        
        "s": {
            "row": 0,
            "col": 2,
            "cost": 99
        },
        
        "a": {
            "row": 2,
            "col": 0,
            "cost": 99
        },
        "b": {
            "row": 2,
            "col": 1,
            "cost": 99
        },
        "c": {
            "row": 2,
            "col": 3,
            "cost": 99
        },
        "e": {
            "row": 4,
            "col": 1,
            "cost": 99
        },
        "d": {
            "row": 4,
            "col": 2,
            "cost": 99
        },
        "f": {
            "row": 5,
            "col": 2,
            "cost": 99
        },
        "g": {
            "row": 6,
            "col": 0,
            "cost": 99
        },
    }

    for node1 in nodes:
        nodes[node1]["cost"] = manhatn_destance(nodes[node1], nodes["g"])

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

    # Use the A* algorithm to find the best path
    start_node = "s"
    goal_node = "g"
    best_path_nodes,solution = astar_search(start_node, goal_node, nodes,edges)
    
 

    if best_path_nodes:
        best_path = []
        spent_cost=0
        best_path_nodes.insert(0,start_node)


    for i, node in enumerate(best_path_nodes):
            if i!=0:
                cost = edges.get("-".join([best_path_nodes[i-1],best_path_nodes[i]]))
            else:
                cost=0
            
            spent_cost+=cost
            remaining_cost = nodes[node]["cost"]
            total_cost = spent_cost + remaining_cost
            
            step_label = f"{node} {spent_cost}-{remaining_cost}-{total_cost}"
            best_path.append(step_label)
            
    return render_template("index.html", nodes=nodes, edges=edges, solutionEdges=solution, bestPath=best_path)

if __name__ == "__main__":
    app.run(debug=True)


