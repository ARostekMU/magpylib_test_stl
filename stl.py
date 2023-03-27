import magpylib as magpy
import trimesh
import pyvista as pv
import numpy as np


stl = trimesh.load('random_object_finer.stl')

magnet = magpy.magnet.TriangularMesh(
    magnetization=(0, 0, 1000),
    vertices=stl.vertices,
    triangles=stl.faces,
)

magnet.show()

grid = pv.UniformGrid(
    dimensions=(200, 200, 200),
    spacing=(0.1, 0.1, 0.1),
    origin=(-10, -10, -10),
)

slice = grid.slice(normal=(1,0,0), origin=(0,0,0))


arr = np.zeros((len(slice.points),3))

import multiprocessing

part_len = 1000

def process_slice(slice, i, arr):
    print(i, '/', len(slice.points)//part_len)
    arr[i*part_len:(i+1)*part_len] = magnet.getB(slice.points[i*part_len:(i+1)*part_len])

if __name__ == '__main__':
    pool = multiprocessing.Pool()
    num_slices = len(slice.points)//part_len
    args = [(slice, i, arr) for i in range(num_slices)]
    pool.starmap(process_slice, args)
    pool.close()
    pool.join()


# This is a workaround so that magpylib does not eat all the memory 
#part_len = 10000
#for i in range(len(slice.points)//part_len):
#    print(i, '/', len(slice.points)//part_len)
#    arr[i*part_len:(i+1)*part_len] = magnet.getB(slice.points[i*part_len:(i+1)*part_len])


slice['B'] = arr #magnet.getB(slice.points)

pl = pv.Plotter(off_screen=True)

pl.add_mesh(slice, scalars='B', cmap="jet")
pl.show_axes()
pl.camera_position = 'yz'
pl.set_background("white")
#pl.show()
pl.screenshot(filename=f"part_len_{part_len}.png", )