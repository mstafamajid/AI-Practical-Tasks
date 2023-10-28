import json
from queue import PriorityQueue
import time
from flask import Flask, render_template


app = Flask(__name__)

solutionEdgeId = 1


def getId():
    global solutionEdgeId
    newId = solutionEdgeId
    solutionEdgeId += 1
    return newId


def manhatn_destance(node1, node2):
# find distance between two nodes by manhatn distance by this rule abs(x1-x2)+abs(y1-y2)
    return abs(node1['row']-node2['row'])+abs(node1['col']-node2['col'])

# Define the A* algorithm function

def astar_search(start, goal, nodes, edges):
    open_set = PriorityQueue()
    open_set.put((nodes[start]["cost"], start))
    came_from = {}
    g_score = {node: float('inf') for node in nodes}
    g_score[start] = 0


    while not open_set.empty():
        _, current = open_set.get()
        if current == goal:
            path = []
            while current in came_from:
                path.insert(0, current)
                current = came_from[current]
            return path # Return both the path and the solution tree

        for neighbor in nodes:
            if neighbor == 's':
                continue
#create keys like this s-a for getting costs from edges dic
            key = "-".join([current, neighbor])
            tentative_g_score = g_score[current] + edges.get((key), float('inf'))
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score = g_score[neighbor] + manhatn_destance(nodes[neighbor], nodes[goal])

                open_set.put((f_score, neighbor))


                

                
         

    return None# Return None if no path is found





@app.route("/", methods=["GET"])
def index():
# nodes
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

   
# real costs
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



    solutionEdges = {
        "id": getId(),
        "label": "1. S 0-17-17",
        "children": [
            {
                "id": getId(),
                "label": "2. A 6-10-16",
                "children": [
                    {
                        "id": getId(),
                        "label": "4. A 12-4-16",
                    }
                ]
            },
            {
                "id": getId(),
                "label": "2. C 10-4-14",
                "children": [
                    {
                        "id": getId(),
                        "label": "3. D 16-2-18",
                    }
                ]
            },
            {
                "id": getId(),
                "label": "2. B 5-13-18",
                "children": [
                    {
                        "id": getId(),
                        "label": "7. E 10-4-15",
                    },
                    {
                        "id": getId(),
                        "label": "7. D 12-2-14",
                    }
                ]
            }
        ]
    }
    
    # Use the A* algorithm to find the best path
    start_node = "s"
    goal_node = "g"
    # set heurisitc distance for each node by manhatn distance
    for node1 in nodes:
        nodes[node1]["cost"] = manhatn_destance(nodes[node1], nodes[goal_node])
    best_path_nodes = astar_search(start_node, goal_node, nodes,edges)
    
  

    
    
    if best_path_nodes:
        best_path = []
        spent_cost=0
        # add start node to the begin of path
        best_path_nodes.insert(0,start_node)

# for creating labels on best path solution cards
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

    return render_template("index.html", nodes=nodes, edges=edges, bestPath=best_path)

if __name__ == "__main__":
    app.run(debug=True)


