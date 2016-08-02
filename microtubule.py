import bpy
from math import *
from mathutils import Vector
from bpy_extras.object_utils import AddObjectHelper, object_data_add

Rm=0.5


D=pi*Rm/sqrt(40)
dth=2*pi/13
dz=3*D/13

mat_alpha = bpy.data.materials.new('alpha_tubulin')
mat_alpha.diffuse_color=(0.9, 0.0, 0.0)

mat_beta = bpy.data.materials.new('beta_tubulin')
mat_beta.diffuse_color=(0.0, 0.0, 0.9)

def makeMicrotubuleStrand(start=Vector((0,0,0)),nBeads=26,isAlphaAtStart=True, axis='z', name="Microtubule"):
    th=0
    zc=0
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
        pv=pv+start
        
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
    alpha_mesh = bpy.data.meshes.new(name=name+"_AlphaVerts")
    alpha_mesh.from_pydata(alpha_verts, alpha_edges, alpha_faces)
    alpha_obj = object_data_add(bpy.context, alpha_mesh)
    
    beta_edges = []
    beta_faces = []
    beta_mesh = bpy.data.meshes.new(name=name+"_BetaVerts")
    beta_mesh.from_pydata(beta_verts, beta_edges, beta_faces)
    beta_obj = object_data_add(bpy.context, beta_mesh)

def makeMicrotubule(startAt, length, axis='z', name="Microtubule"):
    
    start=Vector(startAt)
    nBeads=round(length/dz)

    if axis=='x':
       shift=Vector((D,0,0))
       s1u1c= (start[0], start[1]+Rm, start[2])
       s2u1c= (start[0]+D, start[1]+Rm, start[2])
    elif axis=='y':
       shift=Vector((0,D,0))
       s1u1c= (start[0], start[1], start[2]+Rm)
       s2u1c= (start[0], start[1]+D, start[2]+Rm)
    else:
       shift=Vector((0,0,D))
       s1u1c= (start[0]+Rm, start[1], start[2])
       s2u1c= (start[0]+Rm, start[1]+Rm, start[2]+D)

    bpy.context.scene.cursor_location = (0,0,0)
    makeMicrotubuleStrand(start=start,nBeads=nBeads,isAlphaAtStart=True, axis=axis,name=name+"_Strand1")
    makeMicrotubuleStrand(start=start+shift,nBeads=nBeads,isAlphaAtStart=False, axis=axis,name=name+"_Strand2")
    makeMicrotubuleStrand(start=start+2*shift,nBeads=nBeads,isAlphaAtStart=True, axis=axis,name=name+"_Strand3")

    objects = bpy.data.objects
    bpy.ops.object.select_all(action='DESELECT')
    objects[name+"_Strand1"+"_AlphaVerts"].select = True
    objects[name+"_Strand2"+"_AlphaVerts"].select = True
    objects[name+"_Strand3"+"_AlphaVerts"].select = True
    bpy.context.scene.objects.active = objects[name+"_Strand1"+"_AlphaVerts"]
    bpy.ops.object.join()
    objav=objects[name+"_Strand1"+"_AlphaVerts"]
    objav.name=name+"_AlphaVerts"
    
    bpy.ops.object.select_all(action='DESELECT')
    objects[name+"_Strand1"+"_BetaVerts"].select = True
    objects[name+"_Strand2"+"_BetaVerts"].select = True
    objects[name+"_Strand3"+"_BetaVerts"].select = True
    bpy.context.scene.objects.active = objects[name+"_Strand1"+"_BetaVerts"]
    bpy.ops.object.join()
    objbv=objects[name+"_Strand1"+"_BetaVerts"]
    objbv.name=name+"_BetaVerts"
    
    bpy.ops.object.select_all(action='DESELECT')
    objav.select = True
    bpy.context.scene.cursor_location = s1u1c
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    
    bpy.ops.object.select_all(action='DESELECT')
    objbv.select = True
    bpy.context.scene.cursor_location = s2u1c
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, size=D/2, enter_editmode=True, location=s1u1c)
    bpy.ops.mesh.faces_shade_smooth()
    bpy.ops.object.editmode_toggle()
    bpy.context.object.data.materials.append(mat_alpha)
    objau=bpy.data.objects["Icosphere"]
    objau.name = name+"_AlphaUnit"
    
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, size=D/2, enter_editmode=True, location=s2u1c)
    bpy.ops.mesh.faces_shade_smooth()
    bpy.ops.object.editmode_toggle()
    bpy.context.object.data.materials.append(mat_beta)
    objbu=bpy.data.objects["Icosphere"]
    objbu.name = name+"_BetaUnit"
    
    bpy.ops.object.select_all(action='DESELECT')    
    bpy.context.scene.objects.active = objav
    objau.select = True
    objav.select = True
    bpy.ops.object.parent_set(type='VERTEX')
    objav.dupli_type = 'VERTS'

    bpy.ops.object.select_all(action='DESELECT')    
    bpy.context.scene.objects.active = objbv
    objbu.select = True
    objbv.select = True
    bpy.ops.object.parent_set(type='VERTEX')
    objbv.dupli_type = 'VERTS'
    

Lm=15
r0=(-8 ,-3 ,0)
makeMicrotubule(r0,Lm,'x', name="MT1")

Lm=10
r0=(-7 ,2, 0)
makeMicrotubule(r0,Lm,'x', name="MT2")