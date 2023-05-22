import json

# Load JSON data from file
with open('./examples/elements.json') as f:
    data = json.load(f)


node_id = "7d73925a-f5af-4d8f-8b04-0a3985b21409"

# Search for the specified value of kerml:name
node_data = data[node_id]['data']
node_type = node_data[0]['@type']
node_name = node_id

print(node_data)