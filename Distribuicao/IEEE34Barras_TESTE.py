#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 11:52:30 2020

@author: PPeters
"""

"""
FULL P2P - IEEE 14 BUS
"""


### ...::: IMPORTING PYTHON LIBRARIES/PACKAGES :::... ###

import numpy as np
import pandas as pd
# import gurobipy as gb
import pandapower as pp
from pandapower.plotting.plotly import pf_res_plotly
import pandapower.networks


### ...::: IMPORTING DATA FROM i34bWORK AND AGENT :::... ###

# i34bworkData = pd.read_csv("~/Documents/UFJF/BIC_2019_20/disciplina_mercados/python/i34bworkData.csv")
# #print ('\n\n i34bwork Data:\n', i34bworkData)

# AgentData = pd.read_csv("~/Documents/UFJF/BIC_2019_20/disciplina_mercados/python/AgentData_14_mod.csv")
# #print ('\n\n Agent Data:\n', AgentData)

# ### ...::: PROBLEM DATA :::... ###

# peer_agent = AgentData['Agent']
# peer_bus   = AgentData['Bus']
# peer_type  = AgentData['Type']
# grid_line  = i34bworkData['Line']

# peer_com = AgentData['Community']
# peer_com = pd.to_numeric(peer_com, errors='coerce')       # used to transform data into numeric type

# p_min = AgentData['Pmin']
# p_min = pd.to_numeric(p_min, errors='coerce')       # used to transform data into numeric type

# p_max = AgentData['Pmax']
# p_max = pd.to_numeric(p_max, errors='coerce')       # used to transform data into numeric type

# a_doll_MW2 = AgentData['a ($/MW^2)']
# a_doll_MW2 = pd.to_numeric(a_doll_MW2, errors='coerce')  # used to transform data into numeric type

# b_doll_MW  = AgentData['b ($/MW)']
# b_doll_MW  = pd.to_numeric(b_doll_MW, errors='coerce')   # used to transform data into numeric type

# nbus   = max(peer_bus)        # defines AMOUNT OF BUSES
# ncom   = max(peer_com)        # defines AMOUNT OF COMMUNITIES
# nagent = max(peer_agent)      # defines AMOUNT OF AGENTS = PEERS
# nline  = max(grid_line)       # defines the AMOUNT OF LINES IN THE SYSTEM

# ### ...::: INCIDENCE MATRIX (A) :::... ###

# Inc = np.zeros((nagent,nagent))

# for i in range(0,nagent):
#     for j in range(0,nagent):
#         if (peer_type[i]=='Producer' and peer_type[j]=='Consumer'):
#             Inc[i,j] = Inc[i,j] + 1
#             Inc[j,i] = Inc[i,j]
#         if (peer_type[i]=='Producer' and peer_type[j]=='Grid_Export'):
#             Inc[i,j] = Inc[i,j] + 1
#             Inc[j,i] = Inc[i,j]
#         if (peer_type[i]=='Consumer' and peer_type[j]=='Grid_Import'):
#             Inc[i,j] = Inc[i,j] + 1
#             Inc[j,i] = Inc[i,j]
            
### ...::: GUROBI OPTIMIZATION - FULL P2P :::... ###

# model = gb.Model('mip1') # initiates the optimization model
# model.params.OutputFlag=False # Supress diagnostic ouput
# P_trade = model.addVars(nagent,nagent) # defining variables

# model.update() # Let Gurobi know that we've added variables to the model

# P_peer = [0]*nagent
# for i in range(0,nagent):
#     for j in range(0,nagent):
#         P_peer[i] = P_peer[i] + P_trade[j,i] * Inc[j,i]
        
# # Social Welfare
# SW = 0
# for i in range(0,nagent):
#     SW = SW + b_doll_MW[i] * P_peer[i]
# #    SW = SW + 0.5 * a_doll_MW2[i] * P_peer[i] * P_peer[i] + b_doll_MW[i] * P_peer[i]

# fob = gb.QuadExpr()
# fob = model.setObjective(SW, gb.GRB.MAXIMIZE) # Set the objective function, and indicate that we want to minimize

# ### ADDING CONSTRAINTS

# for ii in range(0,nagent):
#     model.addConstr(P_peer[ii], gb.GRB.LESS_EQUAL, p_max[ii])
#     model.addConstr(P_peer[ii], gb.GRB.GREATER_EQUAL, p_min[ii])

# for ii in range(0,nagent):
#     for jj in range(0,nagent):
#         model.addConstr(P_trade[ii,jj], gb.GRB.EQUAL, P_trade[jj,ii])        
              
# model.update() # Let Gurobi know that we've added constraints to the model
# model.write("full_p2p_ieee14_w_grid.lp") # creates the optimization model file
# model.optimize() # runs optimization

# ### ...::: RESULTS :::...

# i = 0
# Var_value = np.zeros([441])

# if model.status == gb.GRB.Status.OPTIMAL:    
#     print ('\n\n FOUND OBJECTIVE VALUE: {}'.format(model.ObjVal))
#     for res in model.getVars():
#         Var_name = res.varName
#         Var_value[i] = res.x
#         i = i+1
#         print('%s %g' % (res.varName, res.x))

# MATRIZ = Var_value.reshape(21,21)

# P = np.zeros(21)
# Consumer = 0
# Producer = 0

# for i in range(0,20):
#     P[i] = sum(MATRIZ[i,:])
#     if i<11:
#         Consumer = P[i] + Consumer
#     if i>=11 and i<19:
#         Producer += P[i]
    
# print(P)

### ...::: PANDA POWER :::...
i34b = pp.create_empty_network(name='IEEE-34Node',f_hz=60)

# CRIANDO BARRAS
pp.create_bus(i34b, vn_kv=69, name='Slack', index=0, geodata=(-300,0), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)

pp.create_bus(i34b, vn_kv=24.9, name='800', index=800, geodata=(0,0), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='802', index=802, geodata=(300,0), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='802mid', index=8026, geodata=(600,0), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='806', index=806, geodata=(900,0), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='808', index=808, geodata=(1200,0), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)

pp.create_bus(i34b, vn_kv=24.9, name='808mid', index=80810, geodata=(1200,-150), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='810', index=810, geodata=(1200,-300), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)

pp.create_bus(i34b, vn_kv=24.9, name='812', index=812, geodata=(1500,0), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='814', index=814, geodata=(1800,0), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='814r', index=81450, geodata=(1950,0), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='850', index=850, geodata=(2100,0), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='816', index=816, geodata=(2400,0), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='816mid', index=81624, geodata=(2550,0), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)

pp.create_bus(i34b, vn_kv=24.9, name='818', index=818, geodata=(2400,300), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='818mid', index=81820, geodata=(2400,450), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='820', index=820, geodata=(2400,600), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='820mid', index=82022, geodata=(2400,750), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='822', index=822, geodata=(2400,900), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)

pp.create_bus(i34b, vn_kv=24.9, name='824', index=824, geodata=(2700,0), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='824midh', index=82426, geodata=(2850,0), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='826', index=826, geodata=(3000,0), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)

pp.create_bus(i34b, vn_kv=24.9, name='824midv', index=82428, geodata=(2700,-300), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='828', index=828, geodata=(2700,-900), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='828mid', index=82830, geodata=(2850,-900), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='830', index=830, geodata=(3000,-900), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)

pp.create_bus(i34b, vn_kv=24.9, name='854', index=854, geodata=(3300,-900), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='854mid', index=85456, geodata=(3450,-900), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='856', index=856, geodata=(3600,-900), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)

pp.create_bus(i34b, vn_kv=24.9, name='852', index=852, geodata=(3300,-600), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='852r', index=85232, geodata=(3300,-450), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='832', index=832, geodata=(3300,-300), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='832mid', index=83258, geodata=(3300,-150), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='858', index=858, geodata=(3300,0), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)

pp.create_bus(i34b, vn_kv=4.16, name='888', index=888, geodata=(3750,-300), type='b', zone=2, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=4.16, name='890', index=890, geodata=(3900,-300), type='b', zone=2, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)

pp.create_bus(i34b, vn_kv=24.9, name='858midv', index=85864, geodata=(3300,150), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='864', index=864, geodata=(3300,300), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)

pp.create_bus(i34b, vn_kv=24.9, name='858midh', index=85834, geodata=(3450,0), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='834', index=834, geodata=(3600,0), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)

pp.create_bus(i34b, vn_kv=24.9, name='842', index=842, geodata=(3600,300), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='842mid', index=84244, geodata=(3600,450), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='844', index=844, geodata=(3600,600), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='844mid', index=84446, geodata=(3600,750), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='846', index=846, geodata=(3600,900), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='846mid', index=84648, geodata=(3600,1050), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='848', index=848, geodata=(3600,1200), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)

pp.create_bus(i34b, vn_kv=24.9, name='834mid', index=83460, geodata=(3750,0), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='860', index=860, geodata=(3900,0), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='860mid', index=86036, geodata=(4050,0), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='836', index=836, geodata=(4200,0), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='836midh', index=83640, geodata=(4350,0), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='840', index=840, geodata=(4500,0), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)

pp.create_bus(i34b, vn_kv=24.9, name='862', index=862, geodata=(4200,-300), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='862mid', index=86238, geodata=(4200,-450), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(i34b, vn_kv=24.9, name='838', index=838, geodata=(4200,-600), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)


# CRIANDO LINHAS
pp.create_line_from_parameters(i34b, from_bus=0, to_bus=1, length_km=1, r_ohm_per_km=0.01938, x_ohm_per_km=0.05917, c_nf_per_km=388.61, max_i_ka=100, name=None, index=0, type='ol', geodata=None, in_service=True, df=1.0, parallel=1, g_us_per_km=0.0, alpha=None, temperature_degree_celsius=None)
pp.create_line_from_parameters(i34b, from_bus=0, to_bus=4, length_km=1, r_ohm_per_km=0.05403, x_ohm_per_km=0.22304, c_nf_per_km=388.61, max_i_ka=100, name=None, index=1, type='ol', geodata=None, in_service=True, df=1.0, parallel=1, g_us_per_km=0.0, alpha=None, temperature_degree_celsius=None)
pp.create_line_from_parameters(i34b, from_bus=1, to_bus=2, length_km=1, r_ohm_per_km=0.04699, x_ohm_per_km=0.19797, c_nf_per_km=388.61, max_i_ka=100, name=None, index=2, type='ol', geodata=None, in_service=True, df=1.0, parallel=1, g_us_per_km=0.0, alpha=None, temperature_degree_celsius=None)
pp.create_line_from_parameters(i34b, from_bus=1, to_bus=3, length_km=1, r_ohm_per_km=0.05811, x_ohm_per_km=0.17632, c_nf_per_km=388.61, max_i_ka=100, name=None, index=3, type='ol', geodata=None, in_service=True, df=1.0, parallel=1, g_us_per_km=0.0, alpha=None, temperature_degree_celsius=None)
pp.create_line_from_parameters(i34b, from_bus=1, to_bus=4, length_km=1, r_ohm_per_km=0.05695, x_ohm_per_km=0.17388, c_nf_per_km=388.61, max_i_ka=100, name=None, index=4, type='ol', geodata=None, in_service=True, df=1.0, parallel=1, g_us_per_km=0.0, alpha=None, temperature_degree_celsius=None)
pp.create_line_from_parameters(i34b, from_bus=2, to_bus=3, length_km=1, r_ohm_per_km=0.06701, x_ohm_per_km=0.17103, c_nf_per_km=388.61, max_i_ka=100, name=None, index=5, type='ol', geodata=None, in_service=True, df=1.0, parallel=1, g_us_per_km=0.0, alpha=None, temperature_degree_celsius=None)
pp.create_line_from_parameters(i34b, from_bus=3, to_bus=4, length_km=1, r_ohm_per_km=0.01335, x_ohm_per_km=0.04211, c_nf_per_km=0.0, max_i_ka=100, name=None, index=6, type='ol', geodata=None, in_service=True, df=1.0, parallel=1, g_us_per_km=0.0, alpha=None, temperature_degree_celsius=None)
pp.create_line_from_parameters(i34b, from_bus=3, to_bus=6, length_km=1, r_ohm_per_km=0.20912, x_ohm_per_km=0.20912, c_nf_per_km=0.0, max_i_ka=100, name=None, index=7, type='ol', geodata=None, in_service=True, df=1.0, parallel=1, g_us_per_km=0.0, alpha=None, temperature_degree_celsius=None)
pp.create_line_from_parameters(i34b, from_bus=3, to_bus=8, length_km=1, r_ohm_per_km=0.55618, x_ohm_per_km=0.55618, c_nf_per_km=0.0, max_i_ka=100, name=None, index=8, type='ol', geodata=None, in_service=True, df=1.0, parallel=1, g_us_per_km=0.0, alpha=None, temperature_degree_celsius=None)
pp.create_line_from_parameters(i34b, from_bus=4, to_bus=5, length_km=1, r_ohm_per_km=0.25202, x_ohm_per_km=0.25202, c_nf_per_km=0.0, max_i_ka=100, name=None, index=9, type='ol', geodata=None, in_service=True, df=1.0, parallel=1, g_us_per_km=0.0, alpha=None, temperature_degree_celsius=None)
pp.create_line_from_parameters(i34b, from_bus=5, to_bus=10, length_km=1, r_ohm_per_km=0.09498, x_ohm_per_km=0.19890, c_nf_per_km=0.0, max_i_ka=100, name=None, index=10, type='ol', geodata=None, in_service=True, df=1.0, parallel=1, g_us_per_km=0.0, alpha=None, temperature_degree_celsius=None)
pp.create_line_from_parameters(i34b, from_bus=5, to_bus=11, length_km=1, r_ohm_per_km=0.12291, x_ohm_per_km=0.25581, c_nf_per_km=0.0, max_i_ka=100, name=None, index=11, type='ol', geodata=None, in_service=True, df=1.0, parallel=1, g_us_per_km=0.0, alpha=None, temperature_degree_celsius=None)
pp.create_line_from_parameters(i34b, from_bus=5, to_bus=12, length_km=1, r_ohm_per_km=0.06615, x_ohm_per_km=0.13027, c_nf_per_km=0.0, max_i_ka=100, name=None, index=12, type='ol', geodata=None, in_service=True, df=1.0, parallel=1, g_us_per_km=0.0, alpha=None, temperature_degree_celsius=None)
pp.create_line_from_parameters(i34b, from_bus=6, to_bus=7, length_km=1, r_ohm_per_km=0.17615, x_ohm_per_km=0.17615, c_nf_per_km=0.0, max_i_ka=100, name=None, index=13, type='ol', geodata=None, in_service=True, df=1.0, parallel=1, g_us_per_km=0.0, alpha=None, temperature_degree_celsius=None)
pp.create_line_from_parameters(i34b, from_bus=6, to_bus=8, length_km=1, r_ohm_per_km=0.11001, x_ohm_per_km=0.11001, c_nf_per_km=0.0, max_i_ka=100, name=None, index=14, type='ol', geodata=None, in_service=True, df=1.0, parallel=1, g_us_per_km=0.0, alpha=None, temperature_degree_celsius=None)
pp.create_line_from_parameters(i34b, from_bus=8, to_bus=9, length_km=1, r_ohm_per_km=0.03181, x_ohm_per_km=0.08450, c_nf_per_km=0.0, max_i_ka=100, name=None, index=15, type='ol', geodata=None, in_service=True, df=1.0, parallel=1, g_us_per_km=0.0, alpha=None, temperature_degree_celsius=None)
pp.create_line_from_parameters(i34b, from_bus=8, to_bus=13, length_km=1, r_ohm_per_km=0.12711, x_ohm_per_km=0.27038, c_nf_per_km=0.0, max_i_ka=100, name=None, index=16, type='ol', geodata=None, in_service=True, df=1.0, parallel=1, g_us_per_km=0.0, alpha=None, temperature_degree_celsius=None)
pp.create_line_from_parameters(i34b, from_bus=9, to_bus=10, length_km=1, r_ohm_per_km=0.08205, x_ohm_per_km=0.19207, c_nf_per_km=0.0, max_i_ka=100, name=None, index=17, type='ol', geodata=None, in_service=True, df=1.0, parallel=1, g_us_per_km=0.0, alpha=None, temperature_degree_celsius=None)
pp.create_line_from_parameters(i34b, from_bus=11, to_bus=12, length_km=1, r_ohm_per_km=0.22092, x_ohm_per_km=0.19988, c_nf_per_km=0.0, max_i_ka=100, name=None, index=18, type='ol', geodata=None, in_service=True, df=1.0, parallel=1, g_us_per_km=0.0, alpha=None, temperature_degree_celsius=None)
pp.create_line_from_parameters(i34b, from_bus=12, to_bus=13, length_km=1, r_ohm_per_km=0.17093, x_ohm_per_km=0.03802, c_nf_per_km=0.0, max_i_ka=100, name=None, index=19, type='ol', geodata=None, in_service=True, df=1.0, parallel=1, g_us_per_km=0.0, alpha=None, temperature_degree_celsius=None)

# CRIANDO SLACK
pp.create_ext_grid(i34b, bus=0, vm_pu=1.05, va_degree=0.0, max_q_mvar=1.0, min_q_mvar=-1.0, in_service=True, index=0)

# CRIANDO GERADORES
# pp.create_gen(i34b, bus=1, p_mw=P[11], vm_pu=1.0, index=1, max_q_mvar=1.0, min_q_mvar=-1.0, min_p_mw=0., controllable=False, in_service=True)
# pp.create_gen(i34b, bus=2, p_mw=P[12], vm_pu=1.0, index=2, max_q_mvar=1.0, min_q_mvar=-1.0, min_p_mw=0., controllable=False, in_service=True)
# pp.create_gen(i34b, bus=7, p_mw=P[13], vm_pu=1.0, index=3, max_q_mvar=1.0, min_q_mvar=-1.0, min_p_mw=0., controllable=False, in_service=True)
# pp.create_gen(i34b, bus=1, p_mw=P[14], vm_pu=1.0, index=4, max_q_mvar=1.0, min_q_mvar=-1.0, min_p_mw=0., controllable=False, in_service=True)
# pp.create_gen(i34b, bus=5, p_mw=P[15], vm_pu=1.0, index=5, max_q_mvar=1.0, min_q_mvar=-1.0, min_p_mw=0., controllable=False, in_service=True)
# pp.create_gen(i34b, bus=1, p_mw=P[16], vm_pu=1.0, index=6, max_q_mvar=1.0, min_q_mvar=-1.0, min_p_mw=0., controllable=False, in_service=True)
# pp.create_gen(i34b, bus=2, p_mw=P[17], vm_pu=1.0, index=7, max_q_mvar=1.0, min_q_mvar=-1.0, min_p_mw=0., controllable=False, in_service=True)
# pp.create_gen(i34b, bus=7, p_mw=P[18], vm_pu=1.0, index=8, max_q_mvar=1.0, min_q_mvar=-1.0, min_p_mw=0., controllable=False, in_service=True)

# # CRIANDO CARGAS
# pp.create_load(i34b, bus=1, p_mw=P[0], index=1, in_service=True)
# pp.create_load(i34b, bus=2, p_mw=P[1], index=2, in_service=True)
# pp.create_load(i34b, bus=3, p_mw=P[2], index=3, in_service=True)
# pp.create_load(i34b, bus=4, p_mw=P[3], index=4, in_service=True)
# pp.create_load(i34b, bus=5, p_mw=P[4], index=5, in_service=True)
# pp.create_load(i34b, bus=8, p_mw=P[5], index=6, in_service=True)
# pp.create_load(i34b, bus=9, p_mw=P[6], index=7, in_service=True)
# pp.create_load(i34b, bus=10, p_mw=P[7], index=8, in_service=True)
# pp.create_load(i34b, bus=11, p_mw=P[8], index=9, in_service=True)
# pp.create_load(i34b, bus=12, p_mw=P[9], index=10, in_service=True)
# pp.create_load(i34b, bus=13, p_mw=P[10], index=11, in_service=True)

pp.runpp(i34b)
# print(i34b)
# print(i34b.res_bus)
#print(i34b.res_line)
#print(i34b.res_ext_grid)
#print(i34b.res_load)
#print(i34b.res_gen)
pf_res_plotly(i34b, cmap='Jet', use_line_geodata=None, on_map=False, projection=None, map_style='basic', figsize=1, aspectratio='auto', line_width=2, bus_size=10, filename='temp-plot.html')

