import math
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
def run(name, scores, show=True):
    global leaves
    depth = int(math.log2(len(scores)))
    leaves = 0
    mm = minimax(0, 0, True, scores, depth)
    mm_leaves = leaves
    leaves = 0
    log.clear()
    ab = alphabeta(0, 0, True, scores, depth, float('-inf'), float('inf'))
    ab_leaves = leaves
    if show:
        print('\n' + name, scores)
        print('  Minimax    : value', mm, '| leaves evaluated', mm_leaves)
        print('  Alpha-beta : value', ab, '| leaves evaluated', ab_leaves)
        for item in log:
            print('    cut-off at', item[0], 'node (depth', item[1], ', index', item[2], ') after child', item[3],
                  '| alpha =', item[4], '| beta =', item[5], '| leaves skipped:', item[6])
        if depth > 0:
            children = [minimax(1, 0, False, scores, depth), minimax(1, 1, False, scores, depth)]
            print('  Child values (left, right):', children, '| chosen move:', ['left', 'right'][children.index(max(children))])
        print('  Same value:', mm == ab, '| alpha-beta leaves <= minimax leaves:', ab_leaves <= mm_leaves, '| leaves saved:', mm_leaves - ab_leaves)
    return mm, mm_leaves, ab, ab_leaves
print('TASK 2: leaf-evaluation counters for Minimax and Alpha-Beta')
scores = [3, 5, 2, 9, 0, 7]
treeDepth = math.ceil(math.log2(len(scores)))
scores += [0] * (2 ** treeDepth - len(scores))
run('Tree A (Section 5.1 scores, padded with 0)', scores)
run('Tree B (Section 5.2 scores)', [3, 5, 2, 9, 3, 5, 2, 9])
print('\nEdge-case tests')
cases = [('Single leaf', [7]), ('Two leaves', [3, 8]), ('All leaves equal', [4] * 8),
         ('Negative utilities', [-3, -5, -2, -9, -3, -5, -2, -9]), ('Already ordered well', [3, 5, 9, 2, 3, 5, 2, 9])]
for name, s in cases:
    mm, mm_leaves, ab, ab_leaves = run(name, s, False)
    print(' ', name, s, '| minimax', mm, 'with', mm_leaves, 'leaves | alpha-beta', ab, 'with', ab_leaves, 'leaves | same value:', mm == ab)
print('\nPadding test: scores [3, 5, 2, 9, 0, 7] padded with different values')
for pad in [0, float('inf')]:
    s = [3, 5, 2, 9, 0, 7] + [pad] * 2
    mm, mm_leaves, ab, ab_leaves = run('', s, False)
    children = [minimax(1, 0, False, s, 3), minimax(1, 1, False, s, 3)]
    print('  pad =', pad, '| child values', children, '| root value', mm, '| move:', ['left', 'right'][children.index(max(children))],
          '| alpha-beta value', ab, 'with', ab_leaves, 'leaves')
