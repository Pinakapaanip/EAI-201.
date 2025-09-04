print("Helping the rat to escape the underground pipes")
print("Through Depth-First Search (DFS)\n")

def dfs(graph,start,goal):
    st=[[start]]; v=set()
    while st:
        path=st.pop(); node=path[-1]
        if node==goal: return path,v
        if node not in v:
            v.add(node)
            for n,_ in graph.get(node,[]):
                if n not in v: st.append(path+[n])
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
p,v=dfs(graph,s,g)
if p:
    print("\nPath Found")
    print("Path Followed:"," -> ".join(p))
    print("Total Cost (pipes traveled):",len(p)-1)
    print("Total Junctions in Path:",len(p))
    print("Total Junctions Explored by DFS:",len(v))
else: print("No path found")
