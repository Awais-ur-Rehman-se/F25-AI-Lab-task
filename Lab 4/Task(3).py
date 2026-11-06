import heapq
graph = {'S': [('A', 1), ('B', 4)], 'A': [('C', 2)], 'B': [('G', 5)], 'C': [('G', 3)], 'G': []}
h = {'S': 5, 'A': 4, 'B': 4, 'C': 2, 'G': 0}
def tc(n): return 0 if n == 'G' else min(w + tc(x) for x, w in graph[n])
def pc(p): return sum(w for i in range(len(p)-1) for x, w in graph[p[i]] if x == p[i+1])
def astar(h, show=True):
    pq = [(h['S'], 0, 'S', ['S'])]; best = {'S': 0}; pro, exp = [], []
    while pq:
        f, g, n, p = heapq.heappop(pq)
        if g != best[n]: continue
        pro.append(n)
        if n != 'G':
            exp.append(n)
            for x, w in graph[n]:
                if g + w < best.get(x, 9999):
                    best[x] = g + w; heapq.heappush(pq, (g + w + h[x], g + w, x, p + [x]))
        if show:
            fr = ' '.join(f"{x[2]}(g={x[1]},h={h[x[2]]},f={x[0]})" for x in sorted(pq) if x[1] == best[x[2]]) or 'empty'
            print('  processed', n, '| g =', g, 'h =', h[n], 'f =', f); print('     frontier after step:', fr)
        if n == 'G': return p, g, pro, exp
    return None, None, pro, exp
print('TASK 3: overestimating one heuristic value (start S, goal G)')
hb = dict(h); hb['C'] = 10
print('\nSingle change: h(C) from', h['C'], 'to', hb['C'])
print('  True remaining cost of C:', tc('C'), '| overestimate by', hb['C'] - tc('C'))
print('  h(G) is still', hb['G'], '| all other values unchanged')
fail = [n for n in graph if hb[n] > tc(n)]
print('  Admissible after the change:', fail == [], '| nodes that fail:', fail)
print('  Edges that fail consistency:', [(u, v, hb[u], '<=', w + hb[v]) for u in graph for v, w in graph[u] if hb[u] > w + hb[v]])
print('\nOriginal heuristic (h(C) = 2)'); p1, c1, pr1, e1 = astar(h)
print('  Returned path:', p1, '| cost:', pc(p1), '| expansions:', len(e1), e1)
print('\nModified heuristic (h(C) = 10)'); p2, c2, pr2, e2 = astar(hb)
print('  Returned path:', p2, '| cost:', pc(p2), '| expansions:', len(e2), e2)
print('\nComparison\n  Run | path | cost | expansions | expanded nodes | processed order')
print('  h(C)=2 |', '->'.join(p1), '|', pc(p1), '|', len(e1), '|', e1, '|', pr1)
print('  h(C)=10 |', '->'.join(p2), '|', pc(p2), '|', len(e2), '|', e2, '|', pr2)
print('  Path changed:', p1 != p2, '| cost changed:', pc(p1) != pc(p2), '| expansion count changed:', len(e1) != len(e2))
print('  Optimal cost is', tc('S'), '- the modified run returned', pc(p2), '(extra cost', pc(p2) - tc('S'), ')')
print('\nOther single overestimates (extra evidence)')
for n, v in [('B', 10), ('A', 9)]:
    h2 = dict(h); h2[n] = v; p, c, pr, e = astar(h2, False)
    print('  h(' + n + ') =', v, '(true', tc(n), ') ->', '->'.join(p), 'cost', pc(p), '| expansions', len(e), '| optimal:', pc(p) == tc('S'))