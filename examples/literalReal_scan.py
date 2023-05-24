import json

with open('./examples/data/elements.json') as f:
    data = json.load(f)

# Iterate over each object in the "data" array
for obj in data['data']: # not working
    # Check if the object has both "kerml:name" and "kerml:esiData:value" attributes
    if 'kerml:name' in obj and 'kerml:esiData' in obj and 'value' in obj['kerml:esiData']:
        # Extract the values of the attributes
        name = obj['kerml:name']
        value = obj['kerml:esiData']['value']
        
        # Print the values (you can do whatever you want with them)
        print(f"Name: {name}  Value: {value}")
