import heapq

# Heuristic value of each node
nodes = {
        "s": 6,
        "a": 4,
        "b": 4,
        "c": 4,
        "e": 2,
        "d": 2,
        "f": 2,
        "g": 0,
    }

# Cost to move from a node to its connected node
edges = {
    ("s", "a"): 6,
    ("s", "b"): 5,
    ("s", "c"): 10,
    ("a", "e"): 6,
    ("b", "e"): 6,
    ("b", "d"): 7,
    ("c", "d"): 6,
    ("e", "f"): 4,
    ("d", "f"): 6,
    ("f", "g"): 3,
}

start_node = 's'
goal_node = 'g'

def astar(nodes, edges, start, goal):
    open_list = []  # Priority queue for nodes to be evaluated
    came_from = {}  # Dictionary to store the parent node of each node
    g_score = {node: float('inf') for node in nodes}  # Cost from start along best path
    g_score[start] = 0
    f_score = {node: float('inf') for node in nodes}  # Estimated total cost from start to goal through node
    f_score[start] = nodes[start]

    # Push the start node into the priority queue
    heapq.heappush(open_list, (f_score[start], start))

    while open_list:
        current = heapq.heappop(open_list)[1]

        if current == goal:
            # Reconstruct the path from goal to start
            path = []
            while current in came_from:
                path.insert(0, current)
                current = came_from[current]
            path.insert(0, start)
            return path

        for neighbor in nodes:
            if (current, neighbor) in edges:
                tentative_g_score = g_score[current] + edges[(current, neighbor)]
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + nodes[neighbor]
                    if neighbor not in [node[1] for node in open_list]:
                        heapq.heappush(open_list, (f_score[neighbor], neighbor))

    # If no path is found, return None
    return None

path = astar(nodes, edges, start_node, goal_node)
if path:
    print("A* Path:", " -> ".join(path))
else:
    print("No path found.")
