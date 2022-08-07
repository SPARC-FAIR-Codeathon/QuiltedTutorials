from opencmiss.zinc.context import Context
from scaffoldmaker.meshtypes.meshtype_3d_stomach1 import MeshType_3d_stomach1
from opencmiss.zinc.status import OK as ZINC_OK

context = Context("Test")
region = context.getDefaultRegion()
options = MeshType_3d_stomach1.getDefaultOptions(parameterSetName='Rat 1')
x = MeshType_3d_stomach1
z = x.generateBaseMesh(region,options)

fieldmodule = region.getFieldmodule()
field = fieldmodule.findFieldByName("coordinates")

cache = fieldmodule.createFieldcache()
xi = [0.5, 0.5, 0.5]
mesh = fieldmodule.findMeshByDimension(3)
el_iter = mesh.createElementiterator()
element = el_iter.next()
while element.isValid():
    cache.setMeshLocation(element, xi)
    result, outValues = field.evaluateReal(cache, 3)
    # Check result for errors, Use outValues
    if result == ZINC_OK:
        print( element.getIdentifier(), outValues )
    else:
        break
    element = el_iter.next()