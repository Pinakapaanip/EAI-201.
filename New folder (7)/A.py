from queue import PriorityQueue
import math

print("Helping the rat to escape the underground pipes")
print("Through A* Search\n")

def h(n,g,coords):
    x1,y1=coords[n]; x2,y2=coords[g]
    return math.sqrt((x2-x1)**2+(y2-y1)**2)

def astar(graph,start,goal,coords):
    pq=PriorityQueue(); pq.put((0,start))
    cf={start:None}; cs={start:0}; v=set()
    while not pq.empty():
        _,u=pq.get(); v.add(u)
        if u==goal:
            path=[]; 
            while u is not None: path.append(u); u=cf.get(u)
            return path[::-1],cs[goal],v
        for n,w in graph.get(u,[]):
            nc=cs[u]+w
            if n not in cs or nc<cs[n]:
                cs[n]=nc; pq.put((nc+h(n,goal,coords),n)); cf[n]=u
    return None,float("inf"),v

n=int(input("Enter number of junctions (e.g., 5): "))
junctions=[input(f"Enter junction {i+1} name (e.g., A): ").strip() for i in range(n)]
m=int(input("\nEnter number of pipes (e.g., 6): "))
graph={j:[] for j in junctions}
print("Enter pipe connections as: start end cost (e.g., A B 2)")
for i in range(m):
    u,v,c=input(f"Pipe {i+1}: ").split(); c=int(c)
    graph[u].append((v,c)); graph[v].append((u,c))
print("\nEnter coordinates as: name x y (e.g., A 0 5)")
coords={}
for j in junctions:
    e=input(f"Coordinates for {j}: ").split()
    coords[j]=(int(e[1]),int(e[2]))
s=input("\nEnter start junction (e.g., A): ").strip()
g=input("Enter goal junction (e.g., E): ").strip()
p,c,v=astar(graph,s,g,coords)
if p:
    print("\nPath Found")
    print("Path Followed:"," -> ".join(p))
    print("Total Cost of Path:",c)
    print("Total Junctions in Path:",len(p))
    print("Total Junctions Explored by A*:",len(v))
else: print("No path found")
