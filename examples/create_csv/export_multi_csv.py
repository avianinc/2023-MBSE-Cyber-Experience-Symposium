import json
import pandas as pd

filename = './examples/data/rmss_c.json'

# Read the JSON file
with open(filename, 'r') as f:
    data = json.load(f)

print(data['rmss_C']['name'])
print(data['rmss_C']['attributes']['']['attributes'])