from collections import deque

def matching_general(g):
    n = g.n
    match = [-1] * n
    base = list(range(n))
    p = [-1] * n
    used = [False] * n
    blossom = [False] * n
    q = deque()

    def lca(a, b):
        visited = [False] * n
        while True:
            a = base[a]
            visited[a] = True
            if match[a] == -1:
                break
            a = p[match[a]]
        while True:
            b = base[b]
            if visited[b]:
                return b
            b = p[match[b]]

    def mark_path(v, b, children):
        while base[v] != b:
            blossom[base[v]] = blossom[base[match[v]]] = True
            p[v] = children
            children = match[v]
            v = p[match[v]]

    def find_path(root):
        used[:] = [False] * n
        p[:] = [-1] * n
        q.clear()
        q.append(root)
        used[root] = True

        while q:
            v = q.popleft()
            for u in g.vecinos(v):
                if base[v] == base[u] or match[v] == u:
                    continue
                if u == root or (match[u] != -1 and p[match[u]] != -1):
                    cur = lca(v, u)
                    blossom[:] = [False] * n
                    mark_path(v, cur, u)
                    mark_path(u, cur, v)
                    for i in range(n):
                        if blossom[base[i]]:
                            base[i] = cur
                            if not used[i]:
                                used[i] = True
                                q.append(i)
                elif p[u] == -1:
                    p[u] = v
                    if match[u] == -1:
                        while u != -1:
                            v = p[u]
                            w = match[v] if v != -1 else -1
                            match[v] = u
                            match[u] = v
                            u = w
                        return True
                    used[match[u]] = True
                    q.append(match[u])
        return False

    for i in range(n):
        if match[i] == -1:
            base[:] = list(range(n))
            find_path(i)

    res = set()
    for u in range(n):
        v = match[u]
        if v != -1 and u < v:
            res.add((u, v))
    return res
