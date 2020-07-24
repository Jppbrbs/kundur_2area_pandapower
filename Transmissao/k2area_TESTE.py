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


### ...::: IMPORTING DATA FROM netWORK AND AGENT :::... ###

# networkData = pd.read_csv("~/Documents/UFJF/BIC_2019_20/disciplina_mercados/python/networkData.csv")
# #print ('\n\n network Data:\n', networkData)

# AgentData = pd.read_csv("~/Documents/UFJF/BIC_2019_20/disciplina_mercados/python/AgentData_14_mod.csv")
# #print ('\n\n Agent Data:\n', AgentData)

# ### ...::: PROBLEM DATA :::... ###

# peer_agent = AgentData['Agent']
# peer_bus   = AgentData['Bus']
# peer_type  = AgentData['Type']
# grid_line  = networkData['Line']

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
k2area = pp.create_empty_network(name='IEEE-34Node',f_hz=60)


# CRIANDO BARRAS
pp.create_bus(k2area, vn_kv=20*1.03, name='1', index=1, geodata=(-1200,0), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(k2area, vn_kv=20*1.01, name='2', index=2, geodata=(-600,-300), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(k2area, vn_kv=20*1.03, name='3', index=3, geodata=(+1200,0), type='b', zone=2, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(k2area, vn_kv=20*1.01, name='4', index=4, geodata=(+600,-300), type='b', zone=2, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(k2area, vn_kv=230, name='5', index=5, geodata=(-900,0), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(k2area, vn_kv=230, name='6', index=6, geodata=(-600,0), type='b', zone=1, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(k2area, vn_kv=230, name='7', index=7, geodata=(-300,0), type='b', zone=3, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(k2area, vn_kv=230, name='8', index=8, geodata=(0,0), type='b', zone=3, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(k2area, vn_kv=230, name='9', index=9, geodata=(+300,0), type='b', zone=3, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(k2area, vn_kv=230, name='10', index=10, geodata=(+600,0), type='b', zone=2, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)
pp.create_bus(k2area, vn_kv=230, name='11', index=11, geodata=(+900,0), type='b', zone=2, in_service=True, max_vm_pu=1.05, min_vm_pu=0.93, coords=None)


# CRIANDO LINHAS
pp.create_line_from_parameters(k2area, from_bus=6, to_bus=7, length_km=10, r_ohm_per_km=0.0529, x_ohm_per_km=0.529, c_nf_per_km=8.77508, max_i_ka=100, name="10km-B6_B7", index=None, type='ol', geodata=None, in_service=True, df=1.0, parallel=1, g_us_per_km=0.0, alpha=None, temperature_degree_celsius=None)
pp.create_line_from_parameters(k2area, from_bus=10, to_bus=9, length_km=10, r_ohm_per_km=0.0529, x_ohm_per_km=0.529, c_nf_per_km=8.77508, max_i_ka=100, name="10km-B10_B9", index=None, type='ol', geodata=None, in_service=True, df=1.0, parallel=1, g_us_per_km=0.0, alpha=None, temperature_degree_celsius=None)

pp.create_line_from_parameters(k2area, from_bus=5, to_bus=6, length_km=25, r_ohm_per_km=0.0529, x_ohm_per_km=0.529, c_nf_per_km=8.77508, max_i_ka=100, name="25km-B5_B6", index=None, type='ol', geodata=None, in_service=True, df=1.0, parallel=1, g_us_per_km=0.0, alpha=None, temperature_degree_celsius=None)
pp.create_line_from_parameters(k2area, from_bus=11, to_bus=10, length_km=25, r_ohm_per_km=0.0529, x_ohm_per_km=0.529, c_nf_per_km=8.77508, max_i_ka=100, name="25km-B11_B10", index=None, type='ol', geodata=None, in_service=True, df=1.0, parallel=1, g_us_per_km=0.0, alpha=None, temperature_degree_celsius=None)

pp.create_line_from_parameters(k2area, from_bus=7, to_bus=8, length_km=110, r_ohm_per_km=0.0529, x_ohm_per_km=0.529, c_nf_per_km=8.77508, max_i_ka=100, name="110km-B7_B8-1", index=None, type='ol', geodata=None, in_service=True, df=1.0, parallel=2, g_us_per_km=0.0, alpha=None, temperature_degree_celsius=None)
# pp.create_line_from_parameters(k2area, from_bus=7, to_bus=8, length_km=110, r_ohm_per_km=0.0529, x_ohm_per_km=0.529, c_nf_per_km=8.77508, max_i_ka=100, name="110km-B7_B8-2", index=None, type='ol', geodata=None, in_service=True, df=1.0, parallel=1, g_us_per_km=0.0, alpha=None, temperature_degree_celsius=None)
pp.create_line_from_parameters(k2area, from_bus=9, to_bus=8, length_km=110, r_ohm_per_km=0.0529, x_ohm_per_km=0.529, c_nf_per_km=8.77508, max_i_ka=100, name="110km-B9_B8-1", index=None, type='ol', geodata=None, in_service=True, df=1.0, parallel=2, g_us_per_km=0.0, alpha=None, temperature_degree_celsius=None)
# pp.create_line_from_parameters(k2area, from_bus=9, to_bus=8, length_km=110, r_ohm_per_km=0.0529, x_ohm_per_km=0.529, c_nf_per_km=8.77508, max_i_ka=100, name="110km-B9_B8-2", index=None, type='ol', geodata=None, in_service=True, df=1.0, parallel=1, g_us_per_km=0.0, alpha=None, temperature_degree_celsius=None)


# CRIANDO SLACK
pp.create_ext_grid(k2area, name='Slack', bus=4, vm_pu=1.01, va_degree=-17.0, in_service=True, index=None)


# CRIANDO GERADORES
pp.create_gen(k2area, bus=1, p_mw=700, vm_pu=1.03, sn_mva=900, name='G1', index=None, max_q_mvar=99999, min_q_mvar=-99999, min_p_mw=0., controllable=False, in_service=True)
pp.create_gen(k2area, bus=2, p_mw=700, vm_pu=1.01, sn_mva=900, name='G2', index=None, max_q_mvar=99999, min_q_mvar=-99999, min_p_mw=0., controllable=False, in_service=True)
pp.create_gen(k2area, bus=3, p_mw=719, vm_pu=1.03, sn_mva=900, name='G3', index=None, max_q_mvar=99999, min_q_mvar=-99999, min_p_mw=0., controllable=False, in_service=True)
pp.create_gen(k2area, bus=4, p_mw=700, vm_pu=1.01, sn_mva=900, name='G4', index=None, max_q_mvar=99999, min_q_mvar=-99999, min_p_mw=0., controllable=False, in_service=True)


# CRIANDO TRANSFORMADORES
pp.create_transformer_from_parameters(k2area, hv_bus=5, lv_bus=1, name='T1_5', sn_mva=900, vn_hv_kv=230, vn_lv_kv=20*1.03, vk_percent=30.375, vkr_percent=0, pfe_kw=0, i0_percent=0)
pp.create_transformer_from_parameters(k2area, hv_bus=6, lv_bus=2, name='T2_6', sn_mva=900, vn_hv_kv=230, vn_lv_kv=20*1.01, vk_percent=30.375, vkr_percent=0, pfe_kw=0, i0_percent=0)
pp.create_transformer_from_parameters(k2area, hv_bus=11, lv_bus=3, name='T3_11', sn_mva=900, vn_hv_kv=230, vn_lv_kv=20*1.03, vk_percent=30.375, vkr_percent=0, pfe_kw=0, i0_percent=0)
pp.create_transformer_from_parameters(k2area, hv_bus=10, lv_bus=4, name='T4_10', sn_mva=900, vn_hv_kv=230, vn_lv_kv=20*1.01, vk_percent=30.375, vkr_percent=0, pfe_kw=0, i0_percent=0)


# CRIANDO CARGAS
pp.create_load(k2area, bus=1, name='L7', p_mw=967, q_mvar=100, index=7, in_service=True)
pp.create_load(k2area, bus=2, name='L9', p_mw=1767, q_mvar=100, index=9, in_service=True)
pp.create_load(k2area, bus=3, name='C7', p_mw=0, q_mvar=200, index=3, in_service=True)
pp.create_load(k2area, bus=4, name='C9', p_mw=0, q_mvar=350, index=4, in_service=True)


pp.runpp(k2area)
# print(k2area)
# print(k2area.res_bus)
#print(k2area.res_line)
#print(k2area.res_ext_grid)
#print(k2area.res_load)
#print(k2area.res_gen)
pf_res_plotly(k2area, cmap='Jet', use_line_geodata=None, on_map=False, projection=None, map_style='basic', figsize=2, aspectratio='auto', line_width=2, bus_size=10, filename='ieee-13barras.html')

