from flask import Flask, render_template
from aStar import Graph

app = Flask(__name__)

solutionEdgeId = 1
def getId():
    global solutionEdgeId
    newId = solutionEdgeId
    solutionEdgeId += 1
    return newId

@app.route("/", methods=["GET"])
def index():
    nodes = {
        "s":{
            "row":0,
            "col":2,
            "cost":99
        },
        "a":{
            "row":2,
            "col":0,
            "cost":99
        },
        "b":{
            "row":2,
            "col":1,
            "cost":99
        },
        "c":{
            "row":2,
            "col":3,
            "cost":99
        },
        "e":{
            "row":4,
            "col":1,
            "cost":99
        },
        "d":{
            "row":4,
            "col":2,
            "cost":99
        },
        "f":{
            "row":5,
            "col":2,
            "cost":99
        },
        "g":{
            "row":6,
            "col":0,
            "cost":99
        },
    }

    edges = {
        "s-a":6,
        "s-b":5,
        "s-c":10,
        "a-e":6,
        "b-e":6,
        "b-d":7,
        "c-d":6,
        "e-f":4,
        "d-f":6,
        "f-g":3
    }

    # ============================
    # Part 1: using Chebyshev distance
    goal = nodes["g"]
    goal_coordinates = (goal["row"], goal["col"])
    for node_name, node_data in nodes.items():
        node_coordinates = (node_data["row"], node_data["col"])
    
        # Calculate Chebyshev distance
        x_distance = abs(node_coordinates[0] - goal_coordinates[0])
        y_distance = abs(node_coordinates[1] - goal_coordinates[1])
        chebyshev_distance = max(x_distance, y_distance)
    
        # Update the "cost" attribute for the node with the Chebyshev distance
        node_data["cost"] = chebyshev_distance

    # ==============================
    # Part 2: Generate Tree
    def generate_tree(nodes, edges, start_node):
        def tree(node, cost_so_far):
            node_info = nodes[node]
            node_name = node
            heuristic = node_info['cost']
            total_cost = cost_so_far + heuristic
            label = f"{node_name} {cost_so_far}-{heuristic}-{total_cost}"

            children = []
            for edge, edge_cost in edges.items():
                src, dest = edge.split('-')
                if src == node:
                    child_node = tree(dest, cost_so_far + edge_cost)
                    children.append(child_node)

            return {
                "id": getId(),
                "label": label,
                "children": children
            }

        return tree(start_node, 0)

    start_node = "s"
    solutionEdges = generate_tree(nodes, edges, start_node)

    # ===========================================
    # Part 3: A* Algorithim, finding bestPath
    adjacency_list = {}
    heuristics = {}

    # Converting the variables into desired inputs for our class
    # Not for studying
    for node in nodes:
        node_name = node.upper()
        neighbors = []
        
        for edge, cost in edges.items():
            if edge.startswith(node + "-") or edge.endswith("-" + node):
                other_node = edge.replace(node, "").replace("-", "")
                neighbors.append((other_node.upper(), cost))
        
        adjacency_list[node_name] = neighbors
        heuristics[node_name] = abs(nodes[node]['row'] - nodes['g']['row']) + abs(nodes[node]['col'] - nodes['g']['col'])

    graph1 = Graph(adjacency_list, heuristics)
    bestPath = graph1.a_star_algorithm('S', 'G')

    return render_template("index.html", nodes=nodes, edges=edges, solutionEdges=solutionEdges, bestPath=bestPath)

if __name__ == "__main__":
    app.run(debug=True)
