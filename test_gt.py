import graph_tool.all as gt
from numpy.random import seed, random
from scipy.linalg import norm

points = random((5, 2))
points[0] = [0, 0]
points[1] = [1, 1]

g, pos = gt.triangulation(points, type="delaunay")
g.set_directed(True)

# add nodes 
xe1 = g.add_vertex()
xe2 = g.add_vertex()
xe3 = g.add_vertex()
xe4 = g.add_vertex()
dp = g.add_vertex()

v_prop = g.new_vertex_property("string")
v_prop[xe1] = "Xe1"
v_prop[xe2] = "Xe2"
v_prop[xe3] = "Xe3"
v_prop[xe4] = "Xe4"
v_prop[dp] = "DP"

g.vertex_properties["name"]=v_prop 

# add edges
xe1xe2 = g.add_edge(xe1, xe2)
xe2xe1 = g.add_edge(xe2, xe1)

xe2xe3 = g.add_edge(xe2, xe3)
xe2xe2 = g.add_edge(xe3, xe2)

xe4xe2 = g.add_edge(xe4, xe2)
xe2xe4 = g.add_edge(xe2, xe4)

xe4dp = g.add_edge(xe4, dp)
dpxe4 = g.add_edge(dp, xe4)


# reciprocate edges
#for e in edges:
#   g.add_edge(e.target(), e.source())

# The capacity will be defined as the inverse euclidean distance
cap = g.new_edge_property("double")

for e in g.edges():
    print(e)
    cap[e] = random(1) 

g.edge_properties["cap"] = cap
g.vertex_properties["pos"] = pos
g.save("flow-example.xml.gz")
gt.graph_draw(g, pos=pos, vertex_text=g.vertex_properties["name"], edge_pen_width=gt.prop_to_size(cap, mi=0, ma=3, power=1),
              output="flow-example.pdf")
