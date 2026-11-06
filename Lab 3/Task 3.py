import heapq
from collections import deque
GRAPH = {'A': [('B', 1), ('C', 5)], 'B': [('D', 2), ('E', 1)], 'C': [('F', 2), ('G', 7)],
         'D': [], 'E': [('G', 1)], 'F': [], 'G': []}
def ucs(graph, start, goal):
    pq = [(0, 0, start, [start])]
    counter = 0
    done = set()
    trace = []
    while pq:
        cost, _, node, path = heapq.heappop(pq)
        if node in done:
            continue
        done.add(node)
        if node != goal:
            for nxt, w in graph.get(node, []):
                counter += 1
                heapq.heappush(pq, (cost + w, counter, nxt, path + [nxt]))
        frontier = [(n, c) for c, k, n, p in sorted(pq) if n not in done]
        trace.append((node, cost, frontier, path))
        if node == goal:
            return path, cost, trace
    return None, None, trace
def bfs(graph, start, goal):
    q = deque([(start, [start])])
    seen = {start}
    trace = []
    while q:
        node, path = q.popleft()
        if node != goal:
            for nxt, w in graph.get(node, []):
                if nxt not in seen:
                    seen.add(nxt)
                    q.append((nxt, path + [nxt]))
        trace.append((node, [n for n, p in q], path))
        if node == goal:
            return path, trace
    return None, trace
def path_cost(graph, path):
    total = 0
    for a, b in zip(path, path[1:]):
        total += dict(graph[a])[b]
    return total
if __name__ == '__main__':
    print('TASK 3: UCS on the weighted A-G graph (start A, goal G)')
    print('\nEdge weights (nonnegative travel-cost units)')
    for a in GRAPH:
        for b, w in GRAPH[a]:
            print(' ', a, '->', b, '=', w, '(ADDED corridor, Section 3.7)' if (a, b) == ('C', 'G') else '')
    u_path, u_cost, u_trace = ucs(GRAPH, 'A', 'G')
    print('\nUCS trace')
    for step, (node, cost, frontier, p) in enumerate(u_trace, 1):
        print(' ', step, '| processed', node, '| cost', cost, '| frontier (node, cost)', frontier, '| path', '->'.join(p))
    print('  Processing order:', [r[0] for r in u_trace])
    print('  Final path:', u_path, '| hops:', len(u_path) - 1, '| cost by UCS:', u_cost)
    print('  Independent sum of weights:', path_cost(GRAPH, u_path), '| same as UCS:', u_cost == path_cost(GRAPH, u_path))
    b_path, b_trace = bfs(GRAPH, 'A', 'G')
    print('\nBFS on the same weighted topology')
    for step, (node, frontier, p) in enumerate(b_trace, 1):
        print(' ', step, '| processed', node, '| queue (front at left)', frontier, '| path', '->'.join(p))
    print('  Final path:', b_path, '| hops:', len(b_path) - 1, '| cost:', path_cost(GRAPH, b_path))
    print('\nComparison')
    print('  BFS:', b_path, 'hops =', len(b_path) - 1, '| cost =', path_cost(GRAPH, b_path), '| nodes processed =', len(b_trace))
    print('  UCS:', u_path, 'hops =', len(u_path) - 1, '| cost =', path_cost(GRAPH, u_path), '| nodes processed =', len(u_trace))
    print('\nEdge-case tests')
    cyc = {'A': [('B', 1)], 'B': [('A', 1), ('C', 2)], 'C': []}
    print('  Start == goal (A, A):', ucs(GRAPH, 'A', 'A')[:2])
    print('  Unreachable goal (start C, goal E):', ucs(GRAPH, 'C', 'E')[:2])
    print('  Cycle graph A<->B, B->C, goal C:', ucs(cyc, 'A', 'C')[:2])
    print('  Cycle graph, unreachable goal Z:', ucs(cyc, 'A', 'Z')[:2])
    neg = {'A': [('B', 2), ('C', 5)], 'B': [], 'C': [('B', -4)]}
    p, c, t = ucs(neg, 'A', 'B')
    print('\nNegative edge test (A->B=2, A->C=5, C->B=-4, goal B)')
    print('  UCS returned:', p, 'cost', c, '| processing order:', [(r[0], r[1]) for r in t])
    print('  Real cheapest: A->C->B =', path_cost(neg, ['A', 'C', 'B']), '(cheaper than the UCS answer)')
