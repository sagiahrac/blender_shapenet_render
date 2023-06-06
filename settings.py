import os
"""settings.py contains all configuration parameters the blender needs


author baiyu
"""
SHAPENET_BASE_DIR = '/homes/sagiah/school/shapenet/uncompressed/ShapeNetCore.v2'
LOCAL_SHAPENET_BASE_DIR = '/home/mobileye/sagiah/shapenet'


g_shapenet_path = LOCAL_SHAPENET_BASE_DIR
g_blender_excutable_path = '/homes/sagiah/school/blender_shapenet_render/blender-2.79b-linux-glibc219-x86_64/blender'

g_render_objs = [os.environ['SHAPENET_CATEGORY']]
# g_render_objs = ['chair', 'table', 'sofa', 'bed', 'bottle', 'laptop']
# g_render_objs = ['skateboard',
#                 'bottle',
#                 'tower',
#                 'bookshelf',
#                 'camera',
#                 'laptop',
#                 'basket',
#                 'knife',
#                 'can',
#                 'train',
#                 'pillow',
#                 'trash bin',
#                 'mailbox',
#                 'motorbike',
#                 'dishwasher',
#                 'pistol',
#                 'rocket',
#                 'file cabinet',
#                 'bag',
#                 'bed',
#                 'birdhouse',
#                 'piano',
#                 'earphone',
#                 'stove',
#                 'microphone',
#                 'mug',
#                 'remote',
#                 'bowl',
#                 'keyboard',
#                 'washer',
#                 'printer',
#                 'cap',
#                 'helmet',
#                 'microwaves']

#change this path to your background image folder
g_background_image_path = 'background_image'

#folders to store synthetic data
g_syn_rgb_folder = 'syn_rgb'
g_syn_depth_folder = 'syn_depth'
g_syn_pose_folder = 'syn_pose'
g_temp = 'tmp_data'
g_result_dict = 'result.p'

#background image composite
#enum in ['RELATIVE', 'ABSOLUTE', 'SCENE_SIZE', 'RENDER_SIZE'], default 'RELATIVE'
g_scale_space = 'RENDER_SIZE'
g_use_film_transparent = True

#camera:
#enum in ['QUATERNION', 'XYZ', 'XZY', 'YXZ', 'YZX', 'ZXY', 'ZYX', 'AXIS_ANGLE']
g_rotation_mode = 'XYZ'
g_depth_clip_start = 0.5
g_depth_clip_end = 4

#output:

#enum in ['BW', 'RGB', 'RGBA'], default 'BW'
g_rgb_color_mode = 'RGB'
#enum in ['8', '10', '12', '16', '32'], default '8'
g_rgb_color_depth = '16'
g_rgb_file_format = 'PNG'

g_depth_color_mode = 'BW'
g_depth_color_depth = '8'
g_depth_file_format = 'PNG'

g_depth_use_overwrite = True
g_depth_use_file_extension = True

#dimension:

#engine type [CYCLES, BLENDER_RENDER]
g_engine_type = 'CYCLES'

#output image size =  (g_resolution_x * resolution_percentage%, g_resolution_y * resolution_percentage%)
g_resolution_x = 256
g_resolution_y = 256
g_resolution_percentage = 100


#performance:

g_gpu_render_enable = False

#if you are using gpu render, recommand to set hilbert spiral to 256 or 512
#default value for cpu render is fine
g_hilbert_spiral = 512 

#total 55 categories
g_shapenet_categlory_pair = {
    'table' : '04379243',
    'jar' : '03593526',
    'skateboard' : '04225987',
    'car' : '02958343',
    'bottle' : '02876657',
    'tower' : '04460130',
    'chair' : '03001627',
    'bookshelf' : '02871439',
    'camera' : '02942699',
    'airplane' : '02691156',
    'laptop' : '03642806',
    'basket' : '02801938',
    'sofa' : '04256520',
    'knife' : '03624134',
    'can' : '02946921',
    'rifle' : '04090263',
    'train' : '04468005',
    'pillow' : '03938244',
    'lamp' : '03636649',
    'trash bin' : '02747177',
    'mailbox' : '03710193',
    'watercraft' : '04530566',
    'motorbike' : '03790512',
    'dishwasher' : '03207941',
    'bench' : '02828884',
    'pistol' : '03948459',
    'rocket' : '04099429',
    'loudspeaker' : '03691459',
    'file cabinet' : '03337140',
    'bag' : '02773838',
    'cabinet' : '02933112',
    'bed' : '02818832',
    'birdhouse' : '02843684',
    'display' : '03211117',
    'piano' : '03928116',
    'earphone' : '03261776',
    'telephone' : '04401088',
    'stove' : '04330267',
    'microphone' : '03759954',
    'bus' : '02924116',
    'mug' : '03797390',
    'remote' : '04074963',
    'bathtub' : '02808440',
    'bowl' : '02880940',
    'keyboard' : '03085013',
    'guitar' : '03467517',
    'washer' : '04554684',
    'cellular' : '02992529',
    'faucet' : '03325088',
    'printer' : '04004475',
    'cap' : '02954340',
    'clock' : '03046257',
    'helmet' : '03513137',
    'flowerpot' : '03991062',
    'microwaves' : '03761084'
}


max_num_instances = {'02691156': 4045,
                    '02747177': 343,
                    '02773838': 83,
                    '02801938': 113,
                    '02808440': 856,
                    '02818832': 233,
                    '02828884': 1813,
                    '02843684': 73,
                    '02871439': 452,
                    '02876657': 498,
                    '02880940': 186,
                    '02924116': 939,
                    '02933112': 1571,
                    '02942699': 113,
                    '02946921': 108,
                    '02954340': 56,
                    '02958343': 3533,
                    '03001627': 6778,
                    '03046257': 651,
                    '03085013': 65,
                    '03207941': 93,
                    '03211117': 1093,
                    '03261776': 73,
                    '03325088': 744,
                    '03337140': 298,
                    '03467517': 797,
                    '03513137': 162,
                    '03593526': 596,
                    '03624134': 424,
                    '03636649': 2318,
                    '03642806': 460,
                    '03691459': 1597,
                    '03710193': 94,
                    '03759954': 67,
                    '03761084': 152,
                    '03790512': 337,
                    '03797390': 214,
                    '03928116': 239,
                    '03938244': 96,
                    '03948459': 307,
                    '03991062': 602,
                    '04004475': 166,
                    '04074963': 66,
                    '04090263': 2373,
                    '04099429': 85,
                    '04225987': 152,
                    '04256520': 3173,
                    '04330267': 218,
                    '04379243': 8436,
                    '04401088': 1089,
                    '02992529': 831,
                    '04460130': 133,
                    '04468005': 389,
                    '04530566': 1939,
                    '04554684': 169
                    }