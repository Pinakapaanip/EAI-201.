import math

print("Heuristic Function Example (Euclidean Distance)")

def h(n,g,coords):
    x1,y1=coords[n]; x2,y2=coords[g]
    return math.sqrt((x2-x1)**2+(y2-y1)**2)

n=int(input("Enter number of junctions (e.g., 4): "))
junctions=[input(f"Enter junction {i+1} name (e.g., A): ").strip() for i in range(n)]
coords={}
print("\nEnter coordinates as: name x y (e.g., A 0 5)")
for j in junctions:
    e=input(f"Coordinates for {j}: ").split()
    coords[j]=(int(e[1]),int(e[2]))
s=input("\nEnter current junction (e.g., A): ").strip()
g=input("Enter goal junction (e.g., D): ").strip()
print(f"Heuristic distance from {s} to {g}:",h(s,g,coords))
