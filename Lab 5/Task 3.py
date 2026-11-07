import math
from itertools import product
leaves = 0
log = []
def minimax(curDepth, nodeIndex, maxTurn, scores, targetDepth):
    global leaves
    if curDepth == targetDepth:
        leaves = leaves + 1
        return scores[nodeIndex]
    if maxTurn:
        return max(minimax(curDepth + 1, nodeIndex * 2, False, scores, targetDepth),
                   minimax(curDepth + 1, nodeIndex * 2 + 1, False, scores, targetDepth))
    else:
        return min(minimax(curDepth + 1, nodeIndex * 2, True, scores, targetDepth),
                   minimax(curDepth + 1, nodeIndex * 2 + 1, True, scores, targetDepth))
def alphabeta(depth, index, maxTurn, scores, target, alpha, beta):
    global leaves
    if depth == target:
        leaves = leaves + 1
        return scores[index]
    if maxTurn:
        value = float('-inf')
        for i in range(2):
            value = max(value, alphabeta(depth + 1, index * 2 + i, False, scores, target, alpha, beta))
            alpha = max(alpha, value)
            if alpha >= beta:
                log.append(['MAX', depth, index, i, alpha, beta, (1 - i) * 2 ** (target - depth - 1)])
                break
        return value
    else:
        value = float('inf')
        for i in range(2):
            value = min(value, alphabeta(depth + 1, index * 2 + i, True, scores, target, alpha, beta))
            beta = min(beta, value)
            if alpha >= beta:
                log.append(['MIN', depth, index, i, alpha, beta, (1 - i) * 2 ** (target - depth - 1)])
                break
        return value
def count_both(scores):
    global leaves
    depth = int(math.log2(len(scores)))
    leaves = 0
    mm = minimax(0, 0, True, scores, depth)
    mm_leaves = leaves
    leaves = 0
    log.clear()
    ab = alphabeta(0, 0, True, scores, depth, float('-inf'), float('inf'))
    return mm, mm_leaves, ab, leaves
def arrange(seg, node, flags):
    if len(seg) == 1:
        return seg
    mid = len(seg) // 2
    left = arrange(seg[:mid], node * 2 + 1, flags)
    right = arrange(seg[mid:], node * 2 + 2, flags)
    if flags[node]:
        return right + left
    return left + right
def show(label, scores):
    mm, mm_leaves, ab, ab_leaves = count_both(scores)
    print(' ', label, scores, '| minimax', mm, 'with', mm_leaves, 'leaves | alpha-beta', ab, 'with', ab_leaves, 'leaves | same value:', mm == ab)
    for item in log:
        print('      cut-off at', item[0], 'node (depth', item[1], ', index', item[2], ') after child', item[3],
              '| alpha =', item[4], '| beta =', item[5], '| leaves skipped:', item[6])
print('TASK 3: reordering branches, value stays the same, pruning changes')
treeA = [3, 5, 2, 9, 0, 7]
treeA = treeA + [0] * (2 ** math.ceil(math.log2(len(treeA))) - len(treeA))
for name, scores in [('Tree A (Section 5.1, padded)', treeA), ('Tree B (Section 5.2)', [3, 5, 2, 9, 3, 5, 2, 9])]:
    print('\n' + name)
    results = []
    for flags in product([False, True], repeat=7):
        order = arrange(scores, 0, flags)
        mm, mm_leaves, ab, ab_leaves = count_both(order)
        results.append((ab_leaves, order, ab, mm))
    best = results[0]
    worst = results[0]
    for r in results:
        if r[0] < best[0]:
            best = r
        if r[0] > worst[0]:
            worst = r
    print('  Named orderings')
    show('original      ', scores)
    show('mirrored      ', arrange(scores, 0, [True] * 7))
    show('best found    ', best[1])
    show('worst found   ', worst[1])
    print('  All', len(results), 'orderings made by swapping the two children of any nodes')
    print('    root values seen:', sorted(set(r[2] for r in results)), '| minimax equals alpha-beta every time:', all(r[2] == r[3] for r in results))
    counts = {}
    for r in results:
        counts[r[0]] = counts.get(r[0], 0) + 1
    for k in sorted(counts):
        print('    alpha-beta leaves', k, ':', counts[k], 'orderings')
    print('    smallest leaves:', best[0], '| largest leaves:', worst[0], '| minimax leaves: always', len(scores))
