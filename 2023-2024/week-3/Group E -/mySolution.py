from flask import Flask, render_template

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
        "s": {"row": 0, "col": 2, "cost": 99},
        "a": {"row": 2, "col": 0, "cost": 99},
        "b": {"row": 2, "col": 1, "cost": 99},
        "c": {"row": 2, "col": 3, "cost": 99},
        "e": {"row": 4, "col": 1, "cost": 99},
        "d": {"row": 4, "col": 2, "cost": 99},
        "f": {"row": 5, "col": 2, "cost": 99},
        "g": {"row": 6, "col": 0, "cost": 99},
    }

    # Finding the real heuristic values (cost:99)
    # using Chebyshev distance
    goal = nodes["g"]
    goal_coordinates = (goal["row"], goal["col"])
    for node_name, node_data in nodes.items():
        node_coordinates = (node_data["row"], node_data["col"])
    
        # Calculate Chebyshev distance
        x_distance = abs(node_coordinates[0] - goal_coordinates[0])
        y_distance = abs(node_coordinates[1] - goal_coordinates[1])
        chebyshev_distance = max(x_distance, y_distance)
    
        # Update the "cost" attribute for the node with the Chebyshev distance
        nodes[node_name]["cost"] = chebyshev_distance

    # g(n)
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

    def generate_astar_tree(nodes, edges, start_node):
        def astar_tree(node, cost_so_far):
            node_info = nodes[node]
            node_name = node
            heuristic = node_info['cost']
            total_cost = cost_so_far + heuristic
            label = f"{node_name} {cost_so_far}-{heuristic}-{total_cost}"

            children = []
            for edge, edge_cost in edges.items():
                src, dest = edge.split('-')
                if src == node:
                    child_node = astar_tree(dest, cost_so_far + edge_cost)
                    children.append(child_node)

            return {
                "id": getId(),
                "label": label,
                "children": children
            }

        return astar_tree(start_node, 0)
    

    start_node = "s"
    solutionEdges = generate_astar_tree(nodes, edges, start_node)

    def find_best_path(tree):
        if not tree["children"]:
            label = tree["label"]
            return [label]

        best_path = None
        lowest_cost = float("inf")

        for child in tree["children"]:
            path = find_best_path(child)
            if path:
                # Extract the cost from the label
                cost = int(path[0].split()[-1].split('-')[0])
                if cost < lowest_cost:
                    lowest_cost = cost
                    best_path = path
        if best_path:
            label = tree["label"]
            return [label] + best_path

    bestPath = find_best_path(solutionEdges)

    return render_template("index.html", nodes=nodes, edges=edges, solutionEdges=solutionEdges, bestPath=bestPath)

if __name__ == "__main__":
    app.run(debug=True)
