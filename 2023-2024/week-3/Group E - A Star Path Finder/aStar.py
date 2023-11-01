class Graph:
    def __init__(self, adjacency_list, heuristics):
        self.adjacency_list = adjacency_list
        self.heuristics = heuristics

    def get_neighbors(self, node):
        return self.adjacency_list[node]

    def heuristic_value(self, node):
        return self.heuristics[node]

    def a_star_algorithm(self, start_node, stop_node):
        open_set = set([start_node])
        closed_set = set([])

        g_score = {}  # Cost from start along the best path
        f_score = {}  # Estimated total cost from start to goal

        g_score[start_node] = 0
        f_score[start_node] = g_score[start_node] + self.heuristic_value(start_node)

        came_from = {} # Dictionary to store parent nodes.
        came_from[start_node] = start_node

        while len(open_set) > 0:
            current_node = None

            # Find the node with the lowest estimated total cost (f_score).
            for node in open_set:
                if current_node is None or f_score[node] < f_score[current_node]:
                    current_node = node

            if current_node == stop_node:
                path = []
                while came_from[current_node] != current_node:
                    g_value = g_score[current_node]
                    h_value = self.heuristic_value(current_node)
                    f_value = g_value + h_value
                    path.append(f"{current_node} {g_value}-{h_value}-{f_value}")
                    current_node = came_from[current_node]

                path.append(f"{start_node} 0-{self.heuristic_value(start_node)}-{self.heuristic_value(start_node)}")
                path.reverse()

                print('Path found:', path)
                return path

            open_set.remove(current_node)
            closed_set.add(current_node)

            for (neighbor, weight) in self.get_neighbors(current_node):
                tentative_g_score = g_score[current_node] + weight

                if neighbor not in open_set and neighbor not in closed_set:
                    open_set.add(neighbor)
                elif tentative_g_score >= g_score.get(neighbor, float('inf')):
                    continue

                came_from[neighbor] = current_node
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + self.heuristic_value(neighbor)

        print('Path does not exist!')
        return None

# usage example
# adjacency_list = {
#     'S': [('A', 6), ('B', 6)],
#     'A': [('S', 6), ('C', 4)],
#     'B': [('S', 6), ('C', 4)],
#     'C': [('A', 4), ('B', 4),('G', 2)],
#     'G': [('C', 2)]
# }

# heuristics = {
#     'S': 4,
#     'A': 3,
#     'B': 2,
#     'C': 2,
#     'G': 0
# }

# graph1 = Graph(adjacency_list, heuristics)
# graph1.a_star_algorithm('S', 'G')