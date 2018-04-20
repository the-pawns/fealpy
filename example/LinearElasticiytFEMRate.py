import numpy as np
import sys

from fealpy.model.linear_elasticity_model import PolyModel3d, Model2d, SimplifyModel2d, HuangModel2d
from fealpy.mesh.simple_mesh_generator import rectangledomainmesh
from fealpy.femmodel.LinearElasticityFEMModel import LinearElasticityFEMModel 
from fealpy.tools.show import showmultirate

import numpy as np  
import matplotlib.pyplot as plt


m = int(sys.argv[1])
p = int(sys.argv[2])
n = int(sys.argv[3])

if m == 1:
    model = PolyModel3d()
if m == 2:
    model = Model2d()
if m == 3:
    model = SimplifyModel2d()
if m == 4:
    model = HuangModel2d()

#box = [0, 1, 0, 1]
#mesh = rectangledomainmesh(box, nx=n, ny=n)

mesh = model.init_mesh(n)
integrator = mesh.integrator(7)


maxit = 6 

errorType = ['$||\sigma - \sigma_h ||_{0}$',
             '$||div(\sigma - \sigma_h)||_{0}$',
             '$||u - u_h||_{0}$',
             '$||\sigma - \sigma_I ||_{0}$',
             '$||div(\sigma - \sigma_I)||_{0}$'
             ]
Ndof = np.zeros((maxit,))
errorMatrix = np.zeros((len(errorType), maxit), dtype=np.float)

for i in range(maxit):
    fem = LinearElasticityFEMModel(mesh, model, p, integrator)
    #fem.solve()
    fem.fast_solve()
    tgdof = fem.tensorspace.number_of_global_dofs()
    vgdof = fem.vectorspace.number_of_global_dofs()
    gdof = tgdof + vgdof
    Ndof[i] = gdof 
    errorMatrix[:, i] = fem.error()
    if i < maxit - 1:
        mesh.uniform_refine()
        

print('Ndof:', Ndof)
print('error:', errorMatrix)
showmultirate(plt, 1, Ndof, errorMatrix, errorType)
plt.show()
