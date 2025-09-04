from collections import deque

print("Helping the rat to escape the underground pipes")
print("Through Breadth-First Search (BFS)\n")

def bfs(graph,start,goal):
    q=deque([[start]]); v={start}
    while q:
        path=q.popleft(); node=path[-1]
        if node==goal: return path,v
        for n,_ in graph.get(node,[]):
            if n not in v: v.add(n); q.append(path+[n])
    return None,v

n=int(input("Enter number of junctions (e.g., 5): "))
junctions=[input(f"Enter junction {i+1} name (e.g., A): ").strip() for i in range(n)]
m=int(input("\nEnter number of pipes (e.g., 6): "))
graph={j:[] for j in junctions}
print("Enter pipe connections as: start end cost (e.g., A B 2)")
for i in range(m):
    u,v,c=input(f"Pipe {i+1}: ").split(); c=int(c)
    graph[u].append((v,c)); graph[v].append((u,c))
s=input("\nEnter start junction (e.g., A): ").strip()
g=input("Enter goal junction (e.g., E): ").strip()
p,v=bfs(graph,s,g)
if p:
    print("\nPath Found")
    print("Path Followed:"," -> ".join(p))
    print("Total Cost (pipes traveled):",len(p)-1)
    print("Total Junctions in Path:",len(p))
    print("Total Junctions Explored by BFS:",len(v))
else: print("No path found")
