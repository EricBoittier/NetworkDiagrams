import os
import pandas as pd
import numpy as np

f = open("pmfs_210809.dat").readlines()

pd_dict = {}

keys = ["xe1_xe2_1000_forward",
        "xe1_xe2_1000_reverse",
        "xe1_xe2_1001_forward",
        "xe1_xe2_1001_reverse",
        "xe1_xe2_1010_forward",
        "xe1_xe2_1010_reverse",
        "xe1_xe2_1011_forward",
        "xe1_xe2_1011_reverse",

        "xe2_xe3_0100_forward",
        "xe2_xe3_0100_reverse",
        "xe2_xe3_0101_forward",
        "xe2_xe3_0101_reverse",
        "xe2_xe3_1100_forward",
        "xe2_xe3_1100_reverse",
        "xe2_xe3_1011_forward",
        "xe2_xe3_1011_reverse",
        
        "xe4_xe2_0001_forward",
        "xe4_xe2_0001_reverse",
        "xe4_xe2_1001_forward",
        "xe4_xe2_1001_reverse",
        "xe4_xe2_0011_forward",
        "xe4_xe2_0011_reverse",
        "xe4_xe2_1011_forward",
        "xe4_xe2_1011_reverse",
        
        "xe4_dp_0001_forward",
        "xe4_dp_0001_reverse",
        "xe4_dp_0101_forward",
        "xe4_dp_0101_reverse",
        "xe4_dp_1001_forward",
        "xe4_dp_1001_reverse",
        "xe4_dp_1011_forward",
        "xe4_dp_1011_reverse"]


counter = 0 

x = []
y = []

targets = []

for line in f:
   if line.__contains__("@target"):
     targets.append(line)
     if counter != 0:
       k = keys[counter-1]
       p1 = k.split("_")[0]
       p2 = k.split("_")[1]
       state = k.split("_")[2]
       
       assert len(state) == 4, "length of state does not equal 4..."

       direction = k.split("_")[3]

       if direction == "reverse":
         tmp = p1
         p1 = p2
         p2 = tmp

       #  Make sure the state (e.g. [1000]) is correct
       if p1 == "xe1":
         state = "1" + state[1] + state[2] + state[3]
       if p1 == "xe2":
         state = state[0] + "1" + state[2] + state[3]
       if p1 == "xe3":
         state = state[0] + state[1] + "1" + state[3]
       if p1 == "xe4":
         state = state[0] + state[1] + state[2] + "1"
       if p1 == "dp":
         pass  #  currently we don't represent dp in the state...

       if p2 == "xe1":
         state = "0" + state[1] + state[2] + state[3]
       if p2 == "xe2":
         state = state[0] + "0" + state[2] + state[3]
       if p2 == "xe3":
         state = state[0] + state[1] + "0" + state[3]
       if p2 == "xe4":
         state = state[0] + state[1] + state[2] + "0"
       if p2 == "dp":
         pass  #  currently we don't represent dp in the state...
    
       occupancy = state.count("1")
       if occupancy < 1:
         occupancy = 1
       if occupancy == 4:
         occupancy = 3
        
       t = np.column_stack((x, y))
       x_new = t[:,0]
       y_new = t[:,1]
       i_lt02 = np.argwhere(x_new<0.2)
       i_gt08 = np.argwhere(x_new>0.8)

       bound1 = int(max(i_lt02))
       bound2 = int(min(i_gt08))
       y_lt02x = y_new[i_lt02]
       y_gt08x = y_new[i_gt08]
       
       if bound1 < bound2:
         middle = y_new[bound1: bound2]
       else:
         middle = y_new[bound2: bound1]
       print(middle)
       min_1 = np.amin(y_lt02x)
       min_2 = np.amin(y_gt08x) 
       max_1 = np.amax(middle)


       print(counter, targets[counter-1][:-1], "\t\t", k, min_1, min_2, max_1)

      # pd_dict[k] = {"rc": [x], "dG": [y], "state": [state], "key": [k], "p1": [p1], "p2": [p2], "direction": [direction], "min1": [min_1], "min2": [min_2], "max":[max_1], "Ea": [max_1-min_1], "ddG":[min_1-min_2]}  
       pd_dict[k] = {"occupancy": occupancy, "state": "[{}]".format(state), "key": k, "p1": p1, "p2": p2, "direction": direction, "min1":[ min_1], "min2": [min_2], "max": [max_1], "Ea": [max_1-min_1], "ddG":[min_1-min_2]}  
     
     counter += 1
     #  Initialise (and overwrite) variables
     x = []
     y = []  


   else:  #  if line doesn't start with an @ symbol
#     print(targets[-1])
     if not line.startswith("@") and len(line.split()) == 2:
       _x, _y = line.split()
       x.append(float(_x))
       y.append(float(_y))


df = pd.DataFrame(pd_dict)
df.to_csv("pmfs.csv", header=False)

df_tp = df.transpose()



df_tp = df_tp.astype({'state': 'string'})

df_tp = df_tp.sort_values(["occupancy", "state"])



df_tp.to_csv("pmfs_tp.csv")

latex_string = df_tp.to_latex(columns=["occupancy", "state", "p1", "p2", "min1", "min2", "Ea", "ddG"], index=False, float_format="%.2f")

open("latex_table", "w").write(latex_string)


print(df)
print(targets)
