# -*- coding: utf-8 -*-
import unittest
import numpy as np
import vtk
import os
import os.path
from vtk_visualizer import *

src_dir = os.path.dirname(os.path.abspath(str(__file__)))
 
def EstimateNormals(pc): 
    # Differentiate in x direction (dx)
    dxx = np.diff(pc[:,:,0],axis=0)[:,1:]
    dxy = np.diff(pc[:,:,1],axis=0)[:,1:]
    dxz = np.diff(pc[:,:,2],axis=0)[:,1:]
    
    # Differentiate in y direction (dy)
    dyx = np.diff(pc[:,:,0],axis=1)[1:,:]
    dyy = np.diff(pc[:,:,1],axis=1)[1:,:]
    dyz = np.diff(pc[:,:,2],axis=1)[1:,:]
    
    # Calculate normals by cross product of dx*dy
    normals = np.zeros((pc.shape[0],pc.shape[1],3))    
    normals[1:,1:,0] = - dxy * dyz + dxz*dyy;
    normals[1:,1:,1] = - dxz * dyx + dxx*dyz;
    normals[1:,1:,2] = - dxx * dyy + dxy*dyx;
    
    # Normalize length of normals (add a small number to avoid division by 0)
    L = np.sqrt(normals[:,:,0]**2+normals[:,:,1]**2+normals[:,:,2]**2) + 1e-12
    normals[:,:,0] /= L
    normals[:,:,1] /= L
    normals[:,:,2] /= L
        
    return normals

class TestVTKVisualizer(unittest.TestCase):    
    def setUp(self):
        self.vtkControl = get_vtk_control()
        
        h=256; w=256
        
        [y,x] = np.mgrid[0:h,0:w].astype(np.float64)
        z = 10*np.cos(0.1*np.sqrt((x-50)**2+(y-50)**2))
        
        pc = np.zeros((h,w,3))
        pc[:,:,0] = x
        pc[:,:,1] = y
        pc[:,:,2] = z
            
        normals = EstimateNormals(pc)
        
        self.pts = pc.reshape(-1,3)
        self.pts_n = np.dstack([pc,normals])
        self.pts_n = self.pts_n.reshape(-1,6)
                
    def test_pointcloud(self):
        self.vtkControl.AddPointCloudActor(self.pts)

    def test_pointcloud_color(self):
        pts = np.random.rand(1000,6)     
        pts[:,:3] *= 10.0        
        pts[:,3:6] *= 255.0
        self.vtkControl.AddColoredPointCloudActor(pts)
        
    def test_actor(self):
        cone = vtk.vtkConeSource()      
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(cone.GetOutputPort())        
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        self.vtkControl.AddActor(actor)
        
    def test_box(self):
        self.vtkControl.AddBox([-10,-5,-10,-5,-10,0])
        
    def test_axes(self):
        self.vtkControl.AddAxesActor(10.0)
    
    def test_cylinder(self):
        self.vtkControl.AddCylinder((10,0,0),2.0,10.0)        
        
    def test_sphere(self):        
        self.vtkControl.AddSphere((-10,-10,10), 5.0)        
        
    def test_plane(self):
        self.vtkControl.AddPlane() 
        nID = self.vtkControl.GetLastActorID()
        self.vtkControl.SetActorColor(nID,(0,1,0))
        self.vtkControl.SetActorOpacity(nID, 0.5)
        self.vtkControl.SetActorScale(nID, (10,10,0))
        
    def test_hedgehog(self):
        self.vtkControl.AddHedgeHogActor(self.pts_n, 5.0)

    def test_hedgehog_scalars(self):
        pts_n = np.zeros((1000,7))        
        pts_n[:,:2] = np.random.rand(1000,2) * 10.0
        pts_n[:,5] = 1
        self.vtkControl.AddHedgeHogActorWithScalars(pts_n, 5.0)
        
    def test_shaded_points(self):
        self.vtkControl.AddShadedPointsActor(self.pts_n)
        
    def test_normals(self):
        pts_n = np.zeros((1000,6))
        pts_n[:,:2] = np.random.rand(1000,2) * 10.0
        pts_n[:,5] = 1
        self.vtkControl.AddNormalsActor(pts_n, 5.0)
        
    def test_ply(self):
        ply_file = os.path.join(src_dir,'teapot.ply')
        self.vtkControl.AddPLYActor(ply_file)

    def test_stl(self):
        stl_file = os.path.join(src_dir,'teapot.stl')
        self.vtkControl.AddSTLActor(stl_file)
                
if __name__ == '__main__':
       
    suite = unittest.TestLoader().loadTestsFromTestCase(TestVTKVisualizer)
    unittest.TextTestRunner(verbosity=2).run(suite)    
    unittest.main()
