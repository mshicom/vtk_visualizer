# -*- coding: utf-8 -*-
"""
Helper functions for easy visualization of point clouds

.. Author: Øystein Skotheim, SINTEF ICT <oystein.skotheim@sintef.no>
   Date:   Thu Sep 12 15:50:40 2013
"""

import visualizercontrol as vis

g_vtk_control = None
g_hold = False

def get_vtk_control():
    "Get the vtk control currently used by the plot3d functions"
    global g_vtk_control
    
    if g_vtk_control is None:
        g_vtk_control = vis.VTKVisualizerControl()    
        
    return g_vtk_control

def vtkhold(flag=True):
    "Toggle whether new objects will replace previous objects in the visualizer"
    global g_hold
    g_hold = flag
    
def is_hold_enabled():
    "Returns whether hold is enabled"
    global g_hold
    return g_hold
    
def plotxyz(pts):
    """Plot a supplied point cloud (NumPy array of Nxd values where d>=3)
    
    The supplied array may have an additional column with scalars, which
    will be used to color the points (0=black, 1=white)"""
    vtkControl = get_vtk_control()    
    if not is_hold_enabled():
        vtkControl.RemoveAllActors()
    vtkControl.AddPointCloudActor(pts)    
    vtkControl.Render()

def plotxyzrgb(pts):
    "Plot a supplied point cloud w/ color (NumPy array of Nx6 values)"
    vtkControl = get_vtk_control()    
    if not is_hold_enabled():
        vtkControl.RemoveAllActors()
    vtkControl.AddColoredPointCloudActor(pts)    
    vtkControl.Render()

def plothh(pts,scale=5.0):
    "Plot hedge hog (points w/ normals) from given NumPy array of Nx6 values"
    vtkControl = get_vtk_control()    
    if not is_hold_enabled():
        vtkControl.RemoveAllActors()    
    vtkControl.AddHedgeHogActor(pts,scale)
    vtkControl.Render()
    
if __name__ == '__main__':

    import numpy as np
    h, w = 256, 256
    
    [y,x] = np.mgrid[0:h,0:w].astype(np.float64)
    z = 10*np.cos(0.1*np.sqrt((x-w/2.0)**2+(y-h/2.0)**2))
    
    pc = np.zeros((h,w,3))
    pc[:,:,0] = x
    pc[:,:,1] = y
    pc[:,:,2] = z    
    
    pts = pc.reshape(pc.shape[0]*pc.shape[1],pc.shape[2])
    
    plotxyz(pts)