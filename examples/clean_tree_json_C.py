import json
import re

def is_boolean(string):
    return string.lower() in ('true', 'false')

def is_float(string):
    try:
        float(string)
        return '.' in string
    except ValueError:
        return False

def is_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False

def process_dict(d):
    # this function cleans the json data from the treeview removing the instance and name keys
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
# Replace 'file_name.json' with the name of your JSON file
with open('./examples/data/instance_tree.json', 'r') as file:
    data = json.load(file)

processed_data = process_dict(data)

#print(json.dumps(processed_data, indent=2))

# Second procssing step
def separate_uuids(obj, parent_key=None):
    if isinstance(obj, dict):
        new_obj = {}
        for key, value in obj.items():
            match = re.match(r'^(.*?) \((.*?)\)$', key)
            if match:
                new_key, uuid = match.groups()
                new_value = separate_uuids(value, new_key)
                if is_int(new_key):
                    item = {"value": int(new_key), "uuid": uuid}
                    new_key = "Integer"
                elif is_float(new_key):
                    item = {"value": float(new_key), "uuid": uuid}
                    new_key = "Float"
                elif is_boolean(new_key):
                    item = {"value": new_key.lower() == 'true', "uuid": uuid}
                    new_key = "Boolean"
                else:
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
