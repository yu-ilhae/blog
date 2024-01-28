import json
import numpy as np
import random
import copy
import time
import os

RESET_ALL_POSITION=True

NODE_TABLE_PATH = r'.'

INITIAL_MIN_CATEGORY_POSITION_MAGNITUDE = 13
INITIAL_MAX_CATEGORY_POSITION_MAGNITUDE = 20
CATEGORY_MIN_DISTANCE = 20

POST_ANGLE = (-20, 20)
INITIAL_MIN_POST_POSITION_MAGNITUDE = 2
INITIAL_MAX_POST_POSITION_MAGNITUDE = 5
POST_MIN_DISTANCE = 4

def isValidPosition(position):
    if not isinstance(position, list): return False
    if len(position) != 3: return False
    if not isinstance(position[0], float) and not isinstance(position[0], int): return False
    if not isinstance(position[1], float) and not isinstance(position[1], int): return False
    if not isinstance(position[2], float) and not isinstance(position[2], int): return False
    return True

def makeRandomPosition(min_magnitude, max_magnitude):
    magnitude = random.uniform(min_magnitude, max_magnitude)
    position = np.array([random.uniform(-1,1),random.uniform(-1,1),random.uniform(-1,1)])
    position = position / np.linalg.norm(position)
    position = position * magnitude
    return position

def findClosestDistance(target_position, ref_position_array):
    position_array = np.array([p for p in ref_position_array if not np.any(np.isnan(p))])
    if len(position_array) == 0:
        return np.inf
    distance = np.linalg.norm(target_position - position_array, axis=1)
    return np.min(distance)
    
def makeApproximateOrthogonalPosition(base_position, angle_range, min_magnitude, max_magnitude):
    base_position = np.array(base_position)
    if base_position[0] != 0 or base_position[1] != 0:
        orthogonal_position = np.array([-base_position[1], base_position[0], 0])
    else:
        orthogonal_position = np.array([0, -base_position[2], 0])
    orthogonal_position = orthogonal_position / np.linalg.norm(orthogonal_position)

    angle = np.radians(np.random.uniform(0, 360))
    rotation_matrix1 = makeRotationMatrix(base_position, angle)
    
    perpendicular_axis = np.cross(base_position, orthogonal_position)
    angle = np.radians(np.random.uniform(*angle_range))
    rotation_matrix2 = makeRotationMatrix(perpendicular_axis, angle)
    
    magnitude = random.uniform(min_magnitude, max_magnitude)
    
    position = rotation_matrix2 @ rotation_matrix1 @ orthogonal_position
    position = position * magnitude + base_position

    return position


def makeRotationMatrix(axis, theta):
    axis = np.asarray(axis)
    axis = axis / np.sqrt(np.dot(axis, axis))
    a = np.cos(theta / 2.0)
    b, c, d = -axis * np.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa+bb-cc-dd,  2*(bc+ad),      2*(bd-ac)],
                     [2*(bc-ad),    aa+cc-bb-dd,    2*(cd+ab)],
                     [2*(bd+ac),    2*(cd-ab),      aa+dd-bb-cc]])

node_table = None
category_list = None
category_tables = {}

with open(os.path.join(NODE_TABLE_PATH, 'node_table.json'), 'r') as file:
    node_table = json.load(file)
with open(os.path.join(NODE_TABLE_PATH, 'categories', 'category_list.json'), 'r') as file:
    category_list = json.load(file)
for category_name in category_list['categories']:
    with open(os.path.join(NODE_TABLE_PATH, 'categories', category_name, 'node_table.json'), 'r') as file:
        category_tables[category_name] = json.load(file)

for i in range(4, 501):
    sample = copy.deepcopy(node_table['node_list'][1])
    sample['id'] = "category"+str(i)
    sample['url'] = "category"+str(i)+" url"    
    node_table['node_list'].append(sample)
    # node_table['node_list'][0]['connected_node'].append(sample['id'])

with open(os.path.join(NODE_TABLE_PATH, 'node_table.json'), 'w') as file:
    json.dump(node_table, file, indent=4)

categories = []
category_positions = []
for node in node_table['node_list']:
    if node['type'] == 'category':
        categories.append(node)
        if RESET_ALL_POSITION == True:
            category_positions.append(np.array([np.NaN, np.NaN, np.NaN]))
        else:
            if isValidPosition(node['position']):
                category_positions.append(np.array(node['position']))
            else:
                category_positions.append(np.array([np.NaN, np.NaN, np.NaN]))
category_positions = np.array(category_positions)


min_category_position_magnitude = INITIAL_MIN_CATEGORY_POSITION_MAGNITUDE
max_category_position_magnitude = INITIAL_MAX_CATEGORY_POSITION_MAGNITUDE

for idx, category in enumerate(categories):
    if not isValidPosition(category_positions[idx]):
        temp_position_validity = False
        while not temp_position_validity:
            temp_position = makeRandomPosition(min_category_position_magnitude, max_category_position_magnitude)
            min_distance = findClosestDistance(temp_position, category_positions)
            if min_distance > CATEGORY_MIN_DISTANCE:
                category_positions[idx,:] = temp_position
                categories[idx]['position'] = temp_position.tolist()
                temp_position_validity = True
            if random.uniform(0, 1) > 0.5:
                step = random.uniform(0, 1)
                min_category_position_magnitude += step
                max_category_position_magnitude += step

print("category done")

for idx, category in enumerate(categories):

    posts = []
    post_positions = []
    for node in category_tables[category['id']]['node_list']:
        posts.append(node)
        if RESET_ALL_POSITION==True:
            post_positions.append(np.array([np.NaN, np.NaN, np.NaN]))
        else:
            if isValidPosition(node['position']):
                post_positions.append(np.array(node['position']))
            else:
                post_positions.append(np.array([np.NaN, np.NaN, np.NaN]))
    post_positions = np.array(post_positions)
    
    min_post_position_magnitude = INITIAL_MIN_POST_POSITION_MAGNITUDE
    max_post_position_magnitude = INITIAL_MAX_POST_POSITION_MAGNITUDE

    for idx2, post in enumerate(posts):
        if not isValidPosition(post_positions[idx2]):
            temp_position_validity = False
            while not temp_position_validity:
                temp_position = makeApproximateOrthogonalPosition(category['position'], POST_ANGLE, min_post_position_magnitude, max_post_position_magnitude)
                min_distance = findClosestDistance(temp_position, post_positions)
                if min_distance > POST_MIN_DISTANCE:
                    post_positions[idx2,:] = temp_position
                    posts[idx2]['position'] = temp_position.tolist()
                    temp_position_validity = True
                if random.uniform(0, 1) > 0.5:
                    step = random.uniform(0, 1)
                    min_post_position_magnitude += step
                    max_post_position_magnitude += step

    print(idx, "done")

with open(os.path.join(NODE_TABLE_PATH, 'node_table.json'), 'w') as file:
    json.dump(node_table, file, indent=4)
with open(os.path.join(NODE_TABLE_PATH, 'categories', 'category_list.json'), 'w') as file:
    json.dump(category_list, file, indent=4)
for category_name in category_list['categories']:
    with open(os.path.join(NODE_TABLE_PATH, 'categories', category_name, 'node_table.json'), 'w') as file:
        json.dump(category_tables[category_name], file, indent=4)