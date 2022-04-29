#!/usr/bin/env python
# coding: utf-8

# ## Libraries

# In[1]:


# libraries
import numpy as np
import sys
sys.path.append("/home/giovi/programs/EMUstack/backend/")
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pylab as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.interpolate import interp1d

# setup EMUStack paths
import paths
paths.backend_path = '/home/giovi/programs/EMUstack/backend/'
paths.data_path = '/home/giovi/programs/EMUstack/backend/data/'
paths.template_path = '/home/giovi/programs/EMUstack/backend/fortran/msh/'
paths.msh_path = '/home/giovi/Data/electrodynamics/plasmonics/hexagonal_lattice/msh/'

import objects
import materials
import plotting
from stack import *

# importing py-matrix
sys.path.append('/home/giovi/programs/py_matrix/')
import py_matrix as pm

#parallel
import concurrent.futures
get_ipython().run_line_magic('matplotlib', 'inline')


# In[3]:


# light parameters
wl_1 = 300
wl_2 = 1200
n_wl =80
theta_0 = 0.0
phi_0 = 0.0
max_order_PWs = 4

# Set up light objects
v_wl = np.linspace(wl_1,wl_2, n_wl)

# nanodisk array r and pitch in nm
nd_r = 150
nd_p = 500
nd_h = 100

# defining the layers: period must be consistent throughout simulation!!!
NHs = objects.NanoStruct('2D_array', nd_p, 2.0*nd_r, height_nm = nd_h,
    inclusion_a = materials.Air, background = materials.Al, loss = True,
    inc_shape='circle',
    plotting_fields=False,plot_real=1,
    make_mesh_now = True, force_mesh = True, lc_bkg = 0.12, lc2= 5.0, lc3= 3.0,plt_msh=True)#lc_bkg = 0.08, lc2= 5.0)
NHs_mesh_name = NHs.mesh_file

superstrate = objects.ThinFilm(period = nd_p, height_nm = 'semi_inf',
    material = materials.Air, loss = False)
substrate   = objects.ThinFilm(period = nd_p, height_nm = 'semi_inf',
    material = materials.SiO2, loss = False)


# In[6]:


# EMUstack Function
def simulate_stack(wl):

    # define light object
    light = objects.Light(wl, max_order_PWs = max_order_PWs,theta=theta_0,phi=phi_0)
    
    # define structure layer
    NHs = objects.NanoStruct('2D_array', nd_p, 2.0*nd_r, height_nm = nd_h,
                             inclusion_a=materials.Air,
                             background=materials.Al,
                             loss=True,
                             inc_shape='circle',
                             plotting_fields=False,
                             plot_real=1,
                             make_mesh_now=False,mesh_file=NHs_mesh_name)
    superstrate = objects.ThinFilm(period = nd_p, height_nm = 'semi_inf',
                                   material = materials.Air, loss = False)
    substrate   = objects.ThinFilm(period = nd_p, height_nm = 'semi_inf',
                                   material = materials.SiO2, loss = False)
    
    # evaluate each layer individually 
    sim_NHs          = NHs.calc_modes(light)
    sim_superstrate  = superstrate.calc_modes(light)
    sim_substrate    = substrate.calc_modes(light)

    # build the stack solution
    stackSub = Stack((sim_substrate, sim_NHs, sim_superstrate))

    return stackSub


# In[7]:


get_ipython().run_cell_magic('time', '', '# computation\nwith concurrent.futures.ProcessPoolExecutor() as executor:\n    stacks_list = list(executor.map(simulate_stack, v_wl))')


# # Spectra plot

# In[8]:


# spectra
def atr(stacks_list, pol):
    
    a_list = []
    t_list = []
    r_list = []
    for stack in stacks_list:
        stack.calc_scat(pol=pol)
        a_list.extend(stack.a_list)
        t_list.extend(stack.t_list)
        r_list.extend(stack.r_list)
    layers_steps = len(stacks_list[0].layers) - 1
    a_tot      = []
    t_tot      = []
    r_tot      = []
    for i in range(len(v_wl)):
        a_tot.append(float(a_list[layers_steps-1+(i*layers_steps)]))
        t_tot.append(float(t_list[layers_steps-1+(i*layers_steps)]))
        r_tot.append(float(r_list[i]))
        
    return a_tot,t_tot,r_tot


# In[9]:


a_tm,t_tm,r_tm = atr(stacks_list,'TM')
a_te,t_te,r_te = atr(stacks_list,'TE')
a_r,t_r,r_r = atr(stacks_list,'R Circ')
a_l,t_l,r_l = atr(stacks_list,'L Circ')


# In[28]:


# plot
fig, ax = plt.subplots(figsize=(12,8))
f_size = 20

# plot
ax.plot(v_wl,np.array(t_tm),'k',linewidth = 3.0)
ax.plot(v_wl,np.array(t_te),'r--',linewidth = 3.0)
ax.plot(v_wl,np.array(t_r),'ko')
ax.plot(v_wl,np.array(t_l),'rx')

# labels
ax.set_xlabel('Wavelength (nm)',fontsize=f_size)
ax.set_ylabel('T',fontsize=f_size)

# ticks
ax.tick_params(labelsize=f_size)

# legend
ax.legend(['T TM','T TE','T R','T L'], fontsize=f_size)
plt.title('Tranmission',fontsize=f_size);


# In[30]:


# plot
fig, ax = plt.subplots(figsize=(12,8))
f_size = 20

# plot
ax.plot(v_wl,np.array(r_tm),'k',linewidth = 3.0)
ax.plot(v_wl,np.array(r_te),'r--',linewidth = 3.0)
ax.plot(v_wl,np.array(r_r),'ko')
ax.plot(v_wl,np.array(r_l),'rx')

# labels
ax.set_xlabel('Wavelength (nm)',fontsize=f_size)
ax.set_ylabel('R',fontsize=f_size)

# ticks
ax.tick_params(labelsize=f_size)

# legend
ax.legend(['R TM','R TE','R R','R L'], fontsize=f_size)
plt.title('Reflection',fontsize=f_size);


# In[31]:


# plot
fig, ax = plt.subplots(figsize=(12,8))
f_size = 20

# plot
ax.plot(v_wl,np.array(a_tm),'k',linewidth = 3.0)
ax.plot(v_wl,np.array(a_te),'r--',linewidth = 3.0)
ax.plot(v_wl,np.array(a_r),'ko')
ax.plot(v_wl,np.array(a_l),'rx')

# labels
ax.set_xlabel('Wavelength (nm)',fontsize=f_size)
ax.set_ylabel('R',fontsize=f_size)

# ticks
ax.tick_params(labelsize=f_size)

# legend
ax.legend(['A TM','A TE','A R','A L'], fontsize=f_size)
plt.title('Absorption',fontsize=f_size);

