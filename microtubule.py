import bpy
from math import *
from mathutils import Vector
from bpy_extras.object_utils import AddObjectHelper, object_data_add

Rm=0.5
Lm=50
x0=-5.0

D=pi*Rm/sqrt(40)
dth=2*pi/13
dz=3*D/13

mat_alpha = bpy.data.materials.new('alpha_tubulin')
mat_alpha.diffuse_color=(0.9, 0.0, 0.0)

mat_beta = bpy.data.materials.new('beta_tubulin')
mat_beta.diffuse_color=(0.0, 0.0, 0.9)

def makeMicrotubuleStrand(zBottom=0.0,nBeads=26,isAlphaAtStart=True, axis='z'):
    th=0
    zc=zBottom
    snippetLength=0
    isAlpha=isAlphaAtStart
    alpha_verts = []
    beta_verts = []

    for ii in range(1,nBeads):
        xc=Rm*cos(th)
        yc=Rm*sin(th)

        if axis=='x':
           pv=Vector((zc, xc, yc))
        elif axis=='y':
           pv=Vector((yc, zc, xc))
        else:
           pv=Vector((xc, yc, zc))

        if(not isAlpha):
            alpha_verts.append(pv)
        else:
            beta_verts.append(pv)

        snippetLength+=1
        if snippetLength >= 13:
            isAlpha=not isAlpha
            snippetLength=0

        th+=dth
        zc+=dz        

    alpha_edges = []
    alpha_faces = []
    beta_edges = []
    beta_faces = []

    alpha_mesh = bpy.data.meshes.new(name="AlphaVerts")
    alpha_mesh.from_pydata(alpha_verts, alpha_edges, alpha_faces)
    
    beta_mesh = bpy.data.meshes.new(name="BetaVerts")
    beta_mesh.name = "BetaVerts"
    beta_mesh.from_pydata(beta_verts, beta_edges, beta_faces)
    # useful for development when the mesh may be invalid.
    # mesh.validate(verbose=True)
    alpha_obj = object_data_add(bpy.context, alpha_mesh)
    beta_obj = object_data_add(bpy.context, beta_mesh)

def makeMicrotubule(zBottom,length,axis):
    
    nBeads=round(length/dz)
    makeMicrotubuleStrand(zBottom=zBottom,nBeads=nBeads,isAlphaAtStart=True, axis=axis)
    makeMicrotubuleStrand(zBottom=zBottom+D,nBeads=nBeads,isAlphaAtStart=False, axis=axis)
    makeMicrotubuleStrand(zBottom=zBottom+2*D,nBeads=nBeads,isAlphaAtStart=True, axis=axis)

    objects = bpy.data.objects
    bpy.ops.object.select_all(action='DESELECT')
    objects["AlphaVerts"].select = True
    objects["AlphaVerts.001"].select = True
    objects["AlphaVerts.002"].select = True
    bpy.context.scene.objects.active = objects["AlphaVerts"]
    bpy.ops.object.join()
    
    bpy.ops.object.select_all(action='DESELECT')
    objects["BetaVerts"].select = True
    objects["BetaVerts.001"].select = True
    objects["BetaVerts.002"].select = True
    bpy.context.scene.objects.active = objects["BetaVerts"]
    bpy.ops.object.join()
    
    bpy.ops.object.select_all(action='DESELECT')
    objects["AlphaVerts"].select = True
    bpy.context.scene.cursor_location = (Rm, 0, zBottom)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    
    bpy.ops.object.select_all(action='DESELECT')
    objects["BetaVerts"].select = True
    bpy.context.scene.cursor_location = (Rm, 0, zBottom+D)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, size=D/2, enter_editmode=True, location=(Rm, 0, zBottom))
    bpy.ops.mesh.faces_shade_smooth()
    bpy.ops.object.editmode_toggle()
    bpy.context.object.data.materials.append(mat_alpha)
    bpy.data.objects["Icosphere"].name = "AlphaUnit"
    
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, size=D/2, enter_editmode=True, location=(Rm, 0, zBottom+D))
    bpy.ops.mesh.faces_shade_smooth()
    bpy.ops.object.editmode_toggle()
    bpy.context.object.data.materials.append(mat_beta)
    bpy.data.objects["Icosphere"].name = "BetaUnit"
    
    bpy.ops.object.select_all(action='DESELECT')    
    bpy.context.scene.objects.active = objects["AlphaVerts"]
    objects["AlphaUnit"].select = True
    objects["AlphaVerts"].select = True
    bpy.ops.object.parent_set(type='VERTEX')
    objects["AlphaVerts"].dupli_type = 'VERTS'

    bpy.ops.object.select_all(action='DESELECT')    
    bpy.context.scene.objects.active = objects["BetaVerts"]
    objects["BetaUnit"].select = True
    objects["BetaVerts"].select = True
    bpy.ops.object.parent_set(type='VERTEX')
    objects["BetaVerts"].dupli_type = 'VERTS'


makeMicrotubule(x0,Lm,'x')