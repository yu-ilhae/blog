import os
import json
import random
import copy

PATH = './categories'

category_json={
    'categories':[]
}

for i in range(1,21):
    category_json['categories'].append('category'+str(i))

with open(os.path.join(PATH, 'category_list.json'), 'w') as file:
    json.dump(category_json, file, indent=4)
