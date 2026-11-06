graph = {
    'S': [('A', 1), ('B', 4)],
    'A': [('C', 2)],
    'B': [('G', 5)],
    'C': [('G', 3)],
    'G': []
}
h = {'S': 5, 'A': 4, 'B': 4, 'C': 2, 'G': 0}
print("TASK 1: A* Heuristic Audit")
frontier = [('S', 0)]
for step in range(1, 4):
    frontier.sort(key=lambda x: x[1] + h[x[0]])
    node, g = frontier.pop(0)
    f = g + h[node]
    print("\nExpansion", step, ":", node)
    print("g =", g, "h =", h[node], "f =", f)
    for nxt, w in graph[node]:
        ng = g + w
        frontier.append((nxt, ng))
    print("Frontier:", [
        (n, g, h[n], g + h[n]) for n, g in frontier
    ])
print("\nHeuristic Audit:")
true_cost = {'S': 6, 'A': 5, 'B': 5, 'C': 3, 'G': 0}
for n in graph:
    print(n, "Admissible:", h[n] <= true_cost[n])
consistent = True
for u in graph:
    for v, w in graph[u]:
        if h[u] > w + h[v]:
            consistent = False
print("Consistent:", consistent)
print("\nOptimal Path: S -> A -> C -> G")
print("Total Cost: 6")
