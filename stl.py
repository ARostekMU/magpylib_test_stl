import magpylib as magpy
import trimesh
import pyvista as pv


stl = trimesh.load('random_object.stl')

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

slice['B'] = magnet.getB(slice.points)

pl = pv.Plotter()

pl.add_mesh(slice, scalars='B', cmap="jet")
pl.show_axes()
pl.set_background("white")
pl.show()