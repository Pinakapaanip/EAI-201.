from queue import PriorityQueue

print("Helping the rat to escape the underground pipes")
print("Through Uniform Cost Search (UCS)\n")

def ucs(graph,start,goal):
    pq=PriorityQueue(); pq.put((0,start))
    cf={start:None}; cs={start:0}; v=set()
    while not pq.empty():
        c,u=pq.get(); v.add(u)
        if u==goal:
            path=[]; 
            while u is not None: path.append(u); u=cf.get(u)
            return path[::-1],cs[goal],v
        for n,w in graph.get(u,[]):
            nc=cs[u]+w
            if n not in cs or nc<cs[n]:
                cs[n]=nc; pq.put((nc,n)); cf[n]=u
    return None,float("inf"),v

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
p,c,v=ucs(graph,s,g)
if p:
    print("\nPath Found")
    print("Path Followed:"," -> ".join(p))
    print("Total Cost of Path:",c)
    print("Total Junctions in Path:",len(p))
    print("Total Junctions Explored by UCS:",len(v))
else: print("No path found")
