from collections import deque
GRAPH = {'A': ['B', 'C'], 'B': ['D', 'E'], 'C': ['F'],
         'D': [], 'E': ['G'], 'F': [], 'G': []}
def bfs_manual(start, goal, graph=GRAPH):
    q = deque([(start, [start])]); seen = {start}
    while q:
        node, path = q.popleft()
        if node == goal: return path
        for n in graph[node]:
            if n not in seen:
                seen.add(n); q.append((n, path + [n]))
def dfs_manual(start, goal, graph=GRAPH):
    stack = [(start, [start])]; seen = set()
    while stack:
        node, path = stack.pop()
        if node == goal: return path
        if node in seen: continue
        seen.add(node)
        for n in reversed(graph[node]): stack.append((n, path + [n]))
def bfs(graph, start, goal):
    q = deque([(start, [start])])
    seen = {start}
    trace = []
    while q:
        node, path = q.popleft()
        if node != goal:
            for nxt in graph.get(node, []):
                if nxt not in seen:
                    seen.add(nxt)
                    q.append((nxt, path + [nxt]))
        trace.append((node, [n for n, p in q], path))
        if node == goal:
            return path, trace
    return None, trace
def dfs(graph, start, goal):
    stack = [(start, [start])]
    seen = set()
    trace = []
    while stack:
        node, path = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        if node != goal:
            for nxt in reversed(graph.get(node, [])):
                if nxt not in seen:
                    stack.append((nxt, path + [nxt]))
        trace.append((node, [n for n, p in stack], path))
        if node == goal:
            return path, trace
    return None, trace
if __name__ == '__main__':
    print('TASK 1: BFS and DFS on the A-G graph (start A, goal G)')
    results = {}
    for name, fn in [('BFS', bfs), ('DFS', dfs)]:
        path, trace = fn(GRAPH, 'A', 'G')
        results[name] = (path, [r[0] for r in trace])
        label = 'queue (front at left)' if name == 'BFS' else 'stack (top at right)'
        print('\n' + name + ' trace')
        for step, (node, frontier, p) in enumerate(trace, 1):
            print(' ', step, '| processed', node, '|', label, frontier, '| path', '->'.join(p))
        print('  Final path :', path)
        print('  Visit order:', [r[0] for r in trace], '| nodes processed:', len(trace))
    print('\nVerification with supplied manual code')
    print('  BFS path same:', bfs_manual('A', 'G') == results['BFS'][0],
          '| DFS path same:', dfs_manual('A', 'G') == results['DFS'][0])
    print('  BFS order as expected:', results['BFS'][1] == list('ABCDEFG'),
          '| DFS order as expected:', results['DFS'][1] == list('ABDEG'))
    print('\nEdge-case tests')
    cyc = {'A': ['B'], 'B': ['C'], 'C': ['A', 'D'], 'D': []}
    print('  Start == goal (A, A): BFS', bfs(GRAPH, 'A', 'A')[0], '| DFS', dfs(GRAPH, 'A', 'A')[0])
    print('  Unreachable goal (start C, goal D): BFS', bfs(GRAPH, 'C', 'D')[0], '| DFS', dfs(GRAPH, 'C', 'D')[0])
    print('  Cycle graph (A to D): BFS', bfs(cyc, 'A', 'D')[0], '| DFS', dfs(cyc, 'A', 'D')[0])
    print('  Cycle graph, unreachable goal (D to A): BFS', bfs(cyc, 'D', 'A')[0], '| DFS', dfs(cyc, 'D', 'A')[0])
