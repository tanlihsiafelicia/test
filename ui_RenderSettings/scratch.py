import json
import pprint as pp 

# file_path = 'C:/Users/LS0726/Documents/maya/Presets/aaa.json'

def import_json_data(file_path):
    # Open and read the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    return data

# Print the data
pp.pprint(import_json_data(file_path))

# python_dict = {'name': 1, 'attr': 10}

name_list = ['name', 'attr', 'mode']
attr_list = [1, 10, 3]

# print(len(attr_list))

python_dict = {}
# python_dict = {'name': attr_list, 'an': {}}

another_dict = {'a': python_dict}

# print(type(python_dict))

for name, attr in zip(name_list, attr_list):
    print(name, attr)
    python_dict[name] = attr

# for i in range(0, len(name_list)):
#     # assign each items to a temp variable
#     a = name_list[i]
#     b = attr_list[i]
    
#     # append key and value into your dict
#     #{[adding item into your keys]: adding item into the values }
#     python_dict[a] = b

print(python_dict)

# Serializing json
json_object = json.dumps(python_dict, indent=4)

# Writing to sample.json
with open("D:/Temp/sample.json", "w") as outfile:
    outfile.write(json_object)



#################

import json
import pprint as pp 

a = cmds.xform('pSphere1', query=True, rotation=True)

a[0]

geo = 'pSphere1'

attr_name = geo + '.translateX'

b = cmds.listAttr(geo)

name_list = []
attr_list = []
for i in b:
	#print(i)
	if i in ['translateX', 'translateY', 'translateZ']:
		name_list.append(i)

for j in c:
	a = cmds.getAttr(geo + '.' + j)
	attr_list.append(a)
	
# print(len(attr_list))

python_dict = {}
# python_dict = {'name': attr_list, 'an': {}}

another_dict = {'a': python_dict}

# print(type(python_dict))

for name, attr in zip(name_list, attr_list):
    print(name, attr)
    python_dict[name] = attr

# for i in range(0, len(name_list)):
#     # assign each items to a temp variable
#     a = name_list[i]
#     b = attr_list[i]
    
#     # append key and value into your dict
#     #{[adding item into your keys]: adding item into the values }
#     python_dict[a] = b

print(python_dict)

# Serializing json
json_object = json.dumps(python_dict, indent=4)

# Writing to sample.json
with open("D:/Temp/sample.json", "w") as outfile:
    outfile.write(json_object)











