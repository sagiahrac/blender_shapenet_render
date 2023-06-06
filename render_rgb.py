""" render_rgb.py renders obj file to rgb image

Aviable function:
- clear_mash: delete all the mesh in the secene
- scene_setting_init: set scene configurations
- node_setting_init: set node configurations
- render: render rgb image for one obj file and one viewpoint
- render_obj_by_vp_lists: wrapper function for render() render 
                          one obj file by multiple viewpoints
- render_objs_by_one_vp: wrapper function for render() render
                         multiple obj file by one viewpoint
- init_all: a wrapper function, initialize all configurations                          
= set_image_path: reset defualt image output folder

author baiyu
"""
import sys
import os
import random
import pickle
import bpy
import subprocess

abs_path = os.path.abspath(__file__)
sys.path.append(os.path.dirname(abs_path))

from render_helper import *
from settings import *
import settings

def clear_mesh():
    """ clear all meshes in the secene

    """
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            obj.select = True
    bpy.ops.object.delete()

def scene_setting_init(use_gpu):
    """initialize blender setting configurations

    """
    sce = bpy.context.scene.name
    bpy.data.scenes[sce].render.engine = g_engine_type
    bpy.data.scenes[sce].cycles.film_transparent = g_use_film_transparent
    #output
    bpy.data.scenes[sce].render.image_settings.color_mode = g_rgb_color_mode
    bpy.data.scenes[sce].render.image_settings.color_depth = g_rgb_color_depth
    bpy.data.scenes[sce].render.image_settings.file_format = g_rgb_file_format

    #dimensions
    bpy.data.scenes[sce].render.resolution_x = g_resolution_x
    bpy.data.scenes[sce].render.resolution_y = g_resolution_y
    bpy.data.scenes[sce].render.resolution_percentage = g_resolution_percentage
    
    #point light
    light_data = bpy.data.lamps.new(name="PointLight", type='POINT')
    light_object = bpy.data.objects.new(name="PointLight", object_data=light_data)
    bpy.data.scenes[sce].objects.link(light_object)
    light_object.location = (random.randrange(100), random.randrange(100), random.randrange(100))
    light_data.energy = random.randrange(100)
    light_data.shadow_soft_size = random.uniform(0, 2)
    light_data.use_shadow = True
    bpy.data.scenes[sce].objects.active = light_object
    light_object.select = True
        
    if use_gpu:
        bpy.data.scenes[sce].render.engine = 'CYCLES' #only cycles engine can use gpu
        bpy.data.scenes[sce].render.tile_x = g_hilbert_spiral
        bpy.data.scenes[sce].render.tile_x = g_hilbert_spiral
        bpy.types.CyclesRenderSettings.device = 'GPU'
        bpy.data.scenes[sce].cycles.device = 'GPU'

def node_setting_init():
    """node settings for render rgb images

    mainly for compositing the background images
    """


    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree
    links = tree.links

    for node in tree.nodes:
        tree.nodes.remove(node)
    
    image_node = tree.nodes.new('CompositorNodeImage')
    scale_node = tree.nodes.new('CompositorNodeScale')
    alpha_over_node = tree.nodes.new('CompositorNodeAlphaOver')
    render_layer_node = tree.nodes.new('CompositorNodeRLayers')
    file_output_node = tree.nodes.new('CompositorNodeOutputFile')

    scale_node.space = g_scale_space
    file_output_node.base_path = g_syn_rgb_folder

    links.new(image_node.outputs[0], scale_node.inputs[0])
    links.new(scale_node.outputs[0], alpha_over_node.inputs[1])
    links.new(render_layer_node.outputs[0], alpha_over_node.inputs[2])
    links.new(alpha_over_node.outputs[0], file_output_node.inputs[0])

def render(obj_path, viewpoint):
    """render rbg image 

    render a object rgb image by a given camera viewpoint and
    choose random image as background, only render one image
    at a time.

    Args:
        obj_path: a string variable indicate the obj file path
        viewpoint: a vp parameter(contains azimuth,elevation,tilt angles and distance)
    """

    background_images = os.listdir(g_background_image_path)

    vp = viewpoint
    cam_location = camera_location(vp.azimuth, vp.elevation, vp.distance)
    cam_rot = camera_rot_XYZEuler(vp.azimuth, vp.elevation, vp.tilt)

    cam_obj = bpy.data.objects['Camera']
    cam_obj.location[0] = cam_location[0]
    cam_obj.location[1] = cam_location[1]
    cam_obj.location[2] = cam_location[2]

    cam_obj.rotation_euler[0] = cam_rot[0]
    cam_obj.rotation_euler[1] = cam_rot[1]
    cam_obj.rotation_euler[2] = cam_rot[2]

    if not os.path.exists(g_syn_rgb_folder):
        os.mkdir(g_syn_rgb_folder)
    image_name = random.choice(background_images)
    image_path = os.path.join(g_background_image_path, image_name)

    image_node = bpy.context.scene.node_tree.nodes[0]
    image_node.image = bpy.data.images.load(image_path)
    file_output_node = bpy.context.scene.node_tree.nodes[4]
    out_path = 'blender_az{azim}_el{elev}_ti{tilt}_di{dist}-######.color.png'.format(azim=vp.azimuth, elev=vp.elevation, dist=vp.distance, tilt=vp.tilt) # blender placeholder #
    file_output_node.file_slots[0].path = out_path

    #start rendering
    bpy.ops.render.render(write_still=True)

    current_frame = bpy.context.scene.frame_current
    bpy.context.scene.frame_set(current_frame + 1)
    return out_path

def render_obj_by_vp_lists(obj_path, viewpoints):
    """ render one obj file by a given viewpoint list
    a wrapper function for render()

    Args:
        obj_path: a string variable indicate the obj file path
        viewpoints: an iterable object of vp parameter(contains azimuth,elevation,tilt angles and distance)
    """

    if isinstance(viewpoints, tuple):
        vp_lists = [viewpoints]

    try:
        vp_lists = iter(viewpoints)
    except TypeError:
        print("viewpoints is not an iterable object")
    
    for vp in vp_lists:
        render(obj_path, vp)
            
        

def render_objs_by_one_vp(obj_pathes, viewpoint):
    """ render multiple obj files by a given viewpoint

    Args:
        obj_paths: an iterable object contains multiple
                   obj file pathes
        viewpoint: a namedtuple object contains azimuth,
                   elevation,tilt angles and distance
    """ 

    if isinstance(obj_pathes, str):
        obj_lists = [obj_pathes]
    
    try:
        obj_lists = iter(obj_lists)
    except TypeError:
        print("obj_pathes is not an iterable object")
    
    for obj_path in obj_lists:
        render(obj_path, viewpoint)

def init_all():
    """init everything we need for rendering
    an image
    """
    scene_setting_init(g_gpu_render_enable)
    node_setting_init()
    cam_obj = bpy.data.objects['Camera']
    cam_obj.rotation_mode = g_rotation_mode

    bpy.data.objects['Lamp'].data.energy = 50
    bpy.ops.object.lamp_add(type='SUN')

def set_image_path(new_path):
    """ set image output path to new_path

    Args:
        new rendered image output path
    """
    file_output_node = bpy.context.scene.node_tree.nodes[4]
    file_output_node.base_path = new_path

def combine_objects():
    """combine all objects in the scene
    """
    scene = bpy.context.scene
    obs = []

    for ob in scene.objects:
    # whatever objects you want to join...
        if ob.type == 'MESH':
            obs.append(ob)

    ctx = bpy.context.copy()
    # one of the objects to join
    ctx['active_object'] = obs[0]
    ctx['selected_objects'] = obs
    # we need the scene bases as well for joining
    ctx['selected_editable_bases'] = [scene.object_bases[ob.name] for ob in obs]
    bpy.ops.object.join(ctx)

def scale_objects(scale_factor):
    """Scale all mesh objects in the scene, use combine_objects before this
    function
    Args:
        scale_factor: scale percentage
    """
    scene = bpy.context.scene

    for ob in scene.objects:
        ob.select = False
        if ob.type == 'MESH':
            bpy.context.scene.objects.active = ob

    obj = bpy.context.scene.objects.active
    obj.scale = (scale_factor, scale_factor, scale_factor)

### YOU CAN WRITE YOUR OWN IMPLEMENTATION TO GENERATE DATA

init_all()

result_dict = pickle.load(open(os.path.join(g_temp, g_result_dict), 'rb'))
result_list = [result_dict[name] for name in g_render_objs]

for obj_name, models in zip(g_render_objs, result_list):
    obj_folder = os.path.join(g_syn_rgb_folder, obj_name)
    if not os.path.exists(obj_folder):
        os.makedirs(obj_folder)
    
    for idx, model in enumerate(models):
        clear_mesh()
        bpy.ops.import_scene.obj(filepath=model.path)
        #combine_objects()
        #scale_objects(0.5)
        set_image_path(obj_folder)
        render_obj_by_vp_lists(model.path, model.vps)
        if (idx % 100) == 0:
            print("Sync...")
            subprocess.run(["s5cmd", "sync", "syn_rgb", "s3://mobileye-team-angie/users/sagiah/shape/rendered/"])
            subprocess.run(["s5cmd", "rm", "syn_rgb/*"])
            print("Done sync.")
