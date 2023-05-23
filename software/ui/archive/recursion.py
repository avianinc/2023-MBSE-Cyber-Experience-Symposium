import json

#Load the JSON data from the file
with open('input_file.json', 'r') as f:
    json_str = f.read()
    json_str = json_str.replace("'", '"')  # Replace single quotes with double quotes
    json_str = json_str.replace("None", '"None"')
    json_data = json.loads(json_str)

# Access the JSON data
json_items = json_data['data'][1]['kerml:ownedElement']
print(json_items)

# # Create a tree with kerml:name as the root
# tree = {}

# for item in json_items:
#     if 'kerml:name' in item:
#         root = item['kerml:name']
#         tree[root] = []

#     if 'kerml:ownedElement' in item:
#         owned_elements = item['kerml:ownedElement']

#         for element in owned_elements:
#             tree[root].append(element['@id'])

# print(tree)