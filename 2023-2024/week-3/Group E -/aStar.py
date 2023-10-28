class Graph:
    def __init__(self, adjacency_list, heuristics):
        self.adjacency_list = adjacency_list
        self.heuristics = heuristics

    def get_neighbors(self, v):
        return self.adjacency_list[v]

    def h(self, n):
        return self.heuristics[n]

    def a_star_algorithm(self, start_node, stop_node):
        open_list = set([start_node])
        closed_list = set([])

        g = {}
        h_values = {}

        g[start_node] = 0
        h_values[start_node] = self.heuristics[start_node]

        parents = {}
        parents[start_node] = start_node

        while len(open_list) > 0:
            n = None

            for v in open_list:
                if n is None or (g[v] + h_values[v]) < (g[n] + h_values[n]):
                    n = v

            if n is None:
                print('Path does not exist!')
                return None

            if n == stop_node:
                reconst_path = []
                while parents[n] != n:
                    reconst_path.append(f"{n} {g[n]}-{h_values[n]}-{g[n] + h_values[n]}")
                    n = parents[n]

                reconst_path.append(f"{start_node} 0-{h_values[start_node]}-{h_values[start_node]}")
                reconst_path.reverse()

                print('Path found:', reconst_path)
                return reconst_path

            for (m, weight) in self.get_neighbors(n):
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight
                    h_values[m] = self.heuristics[m]

                else:
                    if g[m] > g[n] + weight:
                        g[m] = g[n] + weight
                        parents[m] = n

                        if m in closed_list:
                            closed_list.remove(m)
                            open_list.add(m)

            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None
    
adjacency_list = {
    'S': [('A', 6), ('B', 6)],
    'A': [('S', 6), ('C', 4)],
    'B': [('S', 6), ('C', 4)],
    'C': [('A', 4), ('B', 4),('G', 2)],
    'G': [('C', 2)]
}

heuristics = {
    'S': 4,
    'A': 3,
    'B': 2,
    'C': 2,
    'G': 0
}

# graph1 = Graph(adjacency_list, heuristics)
# graph1.a_star_algorithm('S', 'G')