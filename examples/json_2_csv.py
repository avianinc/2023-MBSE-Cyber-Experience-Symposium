import json
import csv

# Read the JSON file
with open('./examples/data/rmss_b1.json', 'r') as f:
    data = json.load(f)

# Define a recursive function to extract the headers and data
def _recursive_extract(item, row, header_set):
    if isinstance(item, dict):
        for k, v in item.items():
            if isinstance(v, (dict, list)):
                _recursive_extract(v, row, header_set)
            else:
                if k not in header_set:
                    header_set.add(k)
                row.append(v)
        return row
    elif isinstance(item, list):
        for i in item:
            _recursive_extract(i, row, header_set)
        return row

# Extract the header and data
header_set = set()
rows = []
for item in data:
    row = _recursive_extract(item, [], header_set)
    rows.append(row)

header = sorted(list(header_set))
rows.insert(0, header)

# Write the CSV file
with open('./examples/data/rmss_b1.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)
