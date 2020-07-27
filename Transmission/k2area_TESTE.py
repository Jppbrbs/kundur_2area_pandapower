#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#########################################
# Created by: Joao Pedro Peters Barbosa #
#                                       #
# github: https://github.com/Jppbrbs    #
# email: jpptrs@gmail.com               #
#                                       #
# Date: Jul/2020                        #
#########################################


"""
Kundur Two-Area System - pandapower
"""


### ...::: IMPORTING PYTHON LIBRARIES/PACKAGES :::... ###

import numpy as np
import pandas as pd
import pandapower as pp
from pandapower.plotting.plotly import pf_res_plotly
import pandapower.networks




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
pp.create_transformer_from_parameters(k2area, hv_bus=5, lv_bus=1, name='T1_5', sn_mva=900, vn_hv_kv=230, vn_lv_kv=20*1.03, vk_percent=0.135, vkr_percent=0, pfe_kw=0, i0_percent=0)
pp.create_transformer_from_parameters(k2area, hv_bus=6, lv_bus=2, name='T2_6', sn_mva=900, vn_hv_kv=230, vn_lv_kv=20*1.01, vk_percent=0.135, vkr_percent=0, pfe_kw=0, i0_percent=0)
pp.create_transformer_from_parameters(k2area, hv_bus=11, lv_bus=3, name='T3_11', sn_mva=900, vn_hv_kv=230, vn_lv_kv=20*1.03, vk_percent=0.135, vkr_percent=0, pfe_kw=0, i0_percent=0)
pp.create_transformer_from_parameters(k2area, hv_bus=10, lv_bus=4, name='T4_10', sn_mva=900, vn_hv_kv=230, vn_lv_kv=20*1.01, vk_percent=0.135, vkr_percent=0, pfe_kw=0, i0_percent=0)


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
pf_res_plotly(k2area, cmap='Jet', use_line_geodata=None, on_map=False, projection=None, map_style='basic', figsize=2, aspectratio='auto', line_width=2, bus_size=10, filename='kundur2area-pandapower.html')

