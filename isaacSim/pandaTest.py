from pxr import Usd, UsdGeom

import omni


stage = omni.usd.get_context().get_stage()

xformPrim = UsdGeom.Xform.Define(stage, '/hello')

spherePrim = UsdGeom.Sphere.Define(stage, '/hello/world')
