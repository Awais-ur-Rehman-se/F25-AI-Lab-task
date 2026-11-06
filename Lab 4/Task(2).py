import heapq
graph = {
    'S': [('A', 1), ('B', 4)],
    'A': [('C', 2)],
    'B': [('G', 5)],
    'C': [('G', 3)],
    'G': []
}
h = {'S': 5, 'A': 4, 'B': 4, 'C': 2, 'G': 0}
def zero_h(graph):
    return {node: 0 for node in graph}
def path_cost(graph, path):
    total = 0
    for i in range(len(path) - 1):
        for nxt, w in graph[path[i]]:
            if nxt == path[i + 1]:
                total += w
                break
    return total
def astar(graph, h, start, goal):
    pq = [(h[start], 0, start, [start])]
    best = {start: 0}
    processed = []
    expanded = []
    stale = 0
    while pq:
        f, g, node, path = heapq.heappop(pq)
        if g != best.get(node):
            stale += 1
            continue
        processed.append(node)
        if node == goal:
            return path, g, processed, expanded, stale
        expanded.append(node)
        for nxt, w in graph.get(node, []):
            ng = g + w
            if ng < best.get(nxt, float('inf')):
                best[nxt] = ng
                heapq.heappush(
                    pq, (ng + h[nxt], ng, nxt, path + [nxt])
                )
        frontier = [
            (item[2], item[1], h[item[2]], item[0])
            for item in pq
            if item[1] == best[item[2]]
        ]
        print("Processed:", node, "| g =", g,
              "| h =", h[node], "| f =", f)
        print("Frontier:", frontier)
    return None, None, processed, expanded, stale
print("TASK 2: A* AND UCS COMPARISON")
results = []
for name, hh in [('A*', h), ('UCS', zero_h(graph))]:
    print("\n", name)
    path, cost, processed, expanded, stale = astar(
        graph, hh, 'S', 'G'
    )
    print("Returned path:", path)
    print("Search cost:", cost)
    print("Independent path cost:", path_cost(graph, path))
    print("Processed nodes:", processed)
    print("Expanded nodes:", expanded)
    print("Expansion count:", len(expanded))
    print("Stale entries ignored:", stale)
    results.append((name, path, cost, expanded, processed))
print("\nCOMPARISON TABLE")
for name, path, cost, expanded, processed in results:
    print(name, "| Path:", path,
          "| Cost:", cost,
          "| Expansions:", len(expanded),
          "| Processed:", processed)
print("\nEDGE CASE 1: START = GOAL")
path, cost, processed, expanded, stale = astar(
    graph, h, 'S', 'S'
)
print("Path:", path, "Cost:", cost)
print("\nEDGE CASE 2: UNREACHABLE GOAL")
path, cost, processed, expanded, stale = astar(
    graph, h, 'G', 'S'
)
print("Path:", path, "Cost:", cost)
print("\nEDGE CASE 3: STALE ENTRY")
stale_graph = {
    'S': [('A', 4), ('B', 1)],
    'B': [('A', 1)],
    'A': [('C', 3)],
    'C': [('G', 1)],
    'G': []
}
path, cost, processed, expanded, stale = astar(
    stale_graph, zero_h(stale_graph), 'S', 'G'
)
print("Path:", path)
print("Cost:", cost)
print("Stale entries ignored:", stale)
