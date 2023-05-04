import json

def process_dict(d):
    new_dict = {}
    for k, v in d.items():
        if k.lower().startswith('instance') or k.lower().startswith('name') or k.lower().startswith('attributes'):
            if isinstance(v, dict):
                new_dict.update(process_dict(v))
        else:
            if isinstance(v, dict):
                new_dict[k] = process_dict(v)
            else:
                new_dict[k] = v
    return new_dict

# Replace 'file_name.json' with the name of your JSON file
with open('./examples/data/instance_tree.json', 'r') as file:
    data = json.load(file)

processed_data = process_dict(data)

#print(json.dumps(processed_data, indent=2))

# Second procssing step
import json
import re

def separate_uuids(obj, parent_key=None):
    if isinstance(obj, dict):
        new_obj = {}
        for key, value in obj.items():
            match = re.match(r'^(.*?) \((.*?)\)$', key)
            if match:
                new_key, uuid = match.groups()
                new_value = separate_uuids(value, new_key)
                item = {"name": new_key, "uuid": uuid, "attributes": new_value}
            else:
                new_key = key
                new_value = separate_uuids(value, parent_key)
                item = {"name": new_key, "attributes": new_value}
            new_obj[new_key] = item
        return new_obj
    elif isinstance(obj, list):
        return [separate_uuids(item, parent_key) for item in obj]
    else:
        return obj

json_string = processed_data

#json_data = json.loads(json_string)
processed_data = separate_uuids(json_string)

print(json.dumps(processed_data, indent=2))



# Replace 'output_file.json' with the desired output file path
with open('./examples/data/instance_tree_cleaned.json', 'w') as file:
    json.dump(processed_data, file, indent=2)

print(json.dumps(processed_data, indent=2))
