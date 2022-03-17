from graph_tool.all import *
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors


"""
Change for occupation state
"""
#occupation = 3


for occupation in [1, 2, 3]:

  #  create your graph object
  g = Graph()
  
  # Add vertex
  xe1 = g.add_vertex()
  xe2 = g.add_vertex()
  xe3 = g.add_vertex()
  xe4 = g.add_vertex()
  dp = g.add_vertex()
  
  #  Test layout
  #pos = radial_tree_layout(g, g.vertex(1))
  #pos = arf_layout(g, max_iter=0)
  #pos = fruchterman_reingold_layout(g, n_iter=10)
  
  pos = g.new_vertex_property("vector<double>")
  pos[g.vertex(0)] = (0, 0)
  pos[g.vertex(1)] = (1, 1)
  pos[g.vertex(2)] = (2, 0)
  pos[g.vertex(3)] = (1, 2)
  pos[g.vertex(4)] = (1, 3)
  
  
  print(pos)
  
  
  
  #  Create a dictionary to go between labels and vertex objects
  v_dict = {"xe1": xe1, "xe2": xe2, "xe3": xe3, "xe4": xe4, "dp": dp}
  
  #  Add names
  v_prop = g.new_vertex_property("string")
  v_prop[xe1] = "Xe1"
  v_prop[xe2] = "Xe2"
  v_prop[xe3] = "Xe3"
  v_prop[xe4] = "Xe4"
  v_prop[dp] =  "DP"
  #  assign properties as a dic value
  g.vertex_properties["name"]=v_prop 
  
  #  Load DataFrame
  df_orig = pd.read_csv("pmfs_tp.csv")
  
  df = df_orig[df_orig["occupancy"] == occupation]
  
  
  #  edge properties
  
  cap = g.new_edge_property("double")
  state = g.new_edge_property("string")
  edge_color = g.new_edge_property('vector<double>')
  
  #  color map
  cmap = plt.cm.coolwarm
  norm = matplotlib.colors.Normalize(vmin=-3, vmax=3)
  
  max_ddg = max(list(df["ddG"]))
  min_ddg = max(list(df["ddG"]))
  
  
  edge_count = 0
  edge_dict = {}
  
  
  # add edges
  count = 0
  for index, row in df.iterrows():
    print(row)
    edge_dict[edge_count] = g.add_edge(v_dict[row[4]], v_dict[row[5]])
    state[edge_dict[edge_count]] = row[2]
    w = math.exp(-1*float(row[10][1:-1])/(0.001987*300))
    print(row[3], w)
    cap[edge_dict[edge_count]] = w
    c = cmap(norm(float(row[11][1:-1])))
    print(c)
    c = (c[0], c[1], c[2], 0.7)
    edge_color[edge_dict[edge_count]] = c
    count += 1
  
  
  
  graph_draw(
      g, pos=pos,
      vertex_text=g.vertex_properties["name"],
      vertex_font_size=18,
      edge_font_size=10,
      edge_color=edge_color,
      eprops={"text": state},
      edge_pen_width=prop_to_size(cap, mi=2, ma=20, power=1),
      output=f"MbXe_occ_{occupation}.pdf"
  )
  
