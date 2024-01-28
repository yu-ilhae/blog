import os
import json
import random
import copy


def generate_random_hex_color(seed=None):
    if seed is not None:
        random.seed(seed)
    color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    return color


PATH = './categories'
for i in range(1,101):
    os.makedirs(os.path.join(PATH, 'category'+str(i)), exist_ok=True)

    category_json={
        'node_list':[]
    }

    template = {
        'id': 'post',
        'url': 'blank',
        'position':[],
        'color':'#00FF00',
        'type':'post',
        'connected_node':[]
    }

    for j in range(0, random.randint(10,100)):
        sample = copy.deepcopy(template)
        sample['id'] = sample['id']+str(j)
        sample['color'] = generate_random_hex_color(seed=i)
        sample['connected_node'] = ['category'+str(i)]
        category_json['node_list'].append(sample)

    with open(os.path.join(PATH, 'category'+str(i), 'node_table.json'), 'w') as file:
        json.dump(category_json, file, indent=4)
