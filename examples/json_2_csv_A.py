import json
import pandas as pd
import os
from tkinter import filedialog
from tkinter import Tk

# Ask the user to open a JSON file
root = Tk()
root.withdraw()
filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")], title="Open JSON File")

# Read the JSON file
with open(filename, 'r') as f:
    data = json.load(f)

# Get the first key in the dictionary, which is the model name
model_name = list(data.keys())[0]

# Parse rmss_C data
model_data = data[model_name]["attributes"]

# Dynamically build the model dictionary
model = {'Model': model_name}
for attribute_name, attribute_value in model_data['']['attributes'].items():
    model[attribute_name] = attribute_value["attributes"]['parameter']['value']

# Parse hospitals data
hospitals_data = model_data['hospital']['attributes']
hospital_rows = []
for hospital_name in hospitals_data.keys():
    row = {
        'hospitalName': hospital_name,
        'remoteType': hospitals_data[hospital_name]['attributes']['remoteType']['attributes']['parameter']['value'],
        'locX': hospitals_data[hospital_name]['attributes']['locX']['attributes']['parameter']['value'],
        'locY': hospitals_data[hospital_name]['attributes']['locY']['attributes']['parameter']['value'],
        'medCount': hospitals_data[hospital_name]['attributes']['medCount']['attributes']['parameter']['value']
    }
    hospital_rows.append(row)

# Parse drone data
drone_data = model_data['drone']['attributes']
drones_rows = []
for drone_name in drone_data.keys():
    row = {
        'droneName': drone_name,
        'flightRange': drone_data[drone_name]['attributes']['flightRange']['attributes']['parameter']['value'],
        'cargoCapacity': drone_data[drone_name]['attributes']['cargoCapacity']['attributes']['parameter']['value'],
        'speed': drone_data[drone_name]['attributes']['speed']['attributes']['parameter']['value']
    }
    drones_rows.append(row)

# Create DataFrames
model_df = pd.DataFrame([model])
hospitals_df = pd.DataFrame(hospital_rows)
drone_df = pd.DataFrame(drones_rows)

# Ask the user for the folder to save the CSV files
folder_path = filedialog.askdirectory(title="Select Folder to Save CSV Files")

# Save DataFrames to CSV files
model_df.to_csv(os.path.join(folder_path, 'model_data.csv'), index=False)
hospitals_df.to_csv(os.path.join(folder_path, 'hospital_data.csv'), index=False)
drone_df.to_csv(os.path.join(folder_path, 'drone_data.csv'), index=False)
