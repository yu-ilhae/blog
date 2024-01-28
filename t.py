import os
import json
import random
import copy

PATH = './categories'
for i in range(1,501):
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
        sample['connected_node'] = ['category'+str(i)]
        category_json['node_list'].append(sample)

    with open(os.path.join(PATH, 'category'+str(i), 'node_table.json'), 'w') as file:
        json.dump(category_json, file, indent=4)
