from graph_tool.all import *
import math
#create your graph object
g = Graph()

# Add nodes 
xe1 = g.add_vertex()
xe2 = g.add_vertex()
xe3 = g.add_vertex()
xe4 = g.add_vertex()
dp = g.add_vertex()

#  Add names
v_prop = g.new_vertex_property("string")
v_prop[xe1] = "Xe1"
v_prop[xe2] = "Xe2"
v_prop[xe3] = "Xe3"
v_prop[xe4] = "Xe4"
v_prop[dp] = "DP"

#assign properties as a dic value
g.vertex_properties["name"]=v_prop 

# add edges
xe1xe2 = g.add_edge(xe1, xe2)
xe2xe1 = g.add_edge(xe2, xe1)

xe2xe3 = g.add_edge(xe2, xe3)
xe3xe2 = g.add_edge(xe3, xe2)

xe4xe2 = g.add_edge(xe4, xe2)
xe2xe4 = g.add_edge(xe2, xe4)

xe4dp = g.add_edge(xe4, dp)
dpxe4 = g.add_edge(dp, xe4)

print(f"length of edges = {len(list(g.edges()))}")

#  taken from col1 of the PMFs (05.08.2021)
weights = [1.935 - 1, 1.902, 3.043, 3.118, 8.174 - 3, 7.882, 3.839, 5.718]
edges_named = [xe1xe2, xe2xe1, xe2xe3, xe3xe2, xe4xe2, xe2xe4, xe4dp, dpxe4]



cap = g.new_edge_property("double")
state = g.new_edge_property("string")



for w in range(8):
   edge_w = math.exp(-weights[w]/(0.001987*300)) 
   #edge_w = 1/weights[w]
   print(edge_w)
   cap[edges_named[w]] = edge_w
   state[edges_named[w]] = "[1000]"

g.edge_properties["cap"] = cap
g.edge_properties["text"] = state

#draw you graph 
graph_draw(
    g,
    vertex_text=g.vertex_properties["name"],
    vertex_font_size=18,
    eprops={"text": state},
    edge_font_size=10, edge_pen_width=prop_to_size(cap, mi=2, ma=20, power=0.5),
    output="MbXe_test.pdf"
)
