# ExportResultsToCSV

# - Exports a results .aps file to multiple .csv file.
# - Saves the following data:
#   - weather results: {APS_FILE_NAME}_weather.csv
#   - room-level results: {APS_FILE_NAME}_room_level_{ROOM_ID}.csv
#   - apache system misc results: {APS_FILE_NAME}_apache_system_misc_{SYSTEM_ID}.csv
#   - apache system energy results: {APS_FILE_NAME}_apache_system_energy_{SYSTEM_ID}.csv
#   - apache system carbon results: {APS_FILE_NAME}_apache_system_carbon_{SYSTEM_ID}.csv
#   - building load results: {APS_FILE_NAME}_building_loads.csv
#   - building energy results: {APS_FILE_NAME}_building_energy.csv
#   - building carbon results: {APS_FILE_NAME}_building_carbon.csv
#   - surface-level results: {APS_FILE_NAME}_surface_level_{ROOM_ID}_{SURFACE_ID}.csv
#   - opening-level results: {APS_FILE_NAME}_opening_level_{ROOM_ID}_{OPENING_ID}.csv

# 1. Setup
# - import packages
import iesve
import os
import csv
from tkinter import Tk, messagebox
from tkinter.filedialog import askopenfilename
# - instances
current_project = iesve.VEProject.get_current_project()
# - directories
dir_current_project = current_project.path.replace('\\','/')
print('dir_current_project: ', dir_current_project)
assert os.path.exists(dir_current_project), "No IESVE project folder found."
dir_vista = os.path.join(dir_current_project, 'vista')

# 2. Select results file
# - Select file
root = Tk()
root.withdraw()
fp_in = askopenfilename(title = 'Select IES results file', parent = root, initialdir = dir_vista, filetypes = [("APS files","*.aps")])
root.destroy()
print('fp_in: ', fp_in)
# - Exit if filepath is empty string
if fp_in == '': 
    messagebox.showinfo('User input needed', 'Please select a .aps results file.')
    raise Exception("No results .aps file selected.")
# - Exit if filepath is not in project filepath
if not dir_current_project in fp_in:
    messagebox.showinfo('User input needed', 'Please select a .aps results file in the current IES project.')
    raise Exception("Results .aps file selected should be in the current IES project.")

# 3. Export weather data
print('Export weather data', end = ' ')
with iesve.ResultsReader.open(fp_in) as f:
    model_level = 'w'
    variables = [x for x in f.get_variables() if x['model_level'] == model_level]  
        # [dict {'display_name': ..., 'aps_varname': ..., 'units_type': ..., 'model_level': ..., 'subtype': ..., 'custom_type': ..., 'post_process_spec': ...}]
    result = {variable['display_name']: f.get_weather_results(variable['aps_varname'], variable['display_name']) for variable in variables}
    result = {k:[None] * 8760 if v is None else v for k,v in result.items()}   # if any values are `None`, then replace with a list of [None, None, ...]
    fp_out = f'{fp_in[:-4]}_weather.csv'
    with open(fp_out, 'w', newline = '') as f1:
        csvwriter = csv.writer(f1)
        csvwriter.writerow(list(result))
        for row in zip(*list(result.values())):
            csvwriter.writerow(row)
print()

# 4. Export room-level data
print('Export room-level data', end = ' ')
with iesve.ResultsReader.open(fp_in) as f:
    model_level = 'z'
    variables = [x for x in f.get_variables() if x['model_level'] == model_level]  
    for room_id in f.get_room_ids():
        print(room_id, end = ' ')
        result = {variable['display_name']: f.get_room_results(room_id, variable['aps_varname'], variable['display_name'], model_level) for variable in variables}
        result = {k:[None] * 8760 if v is None else v for k,v in result.items()} 
        fp_out = f'{fp_in[:-4]}_room_level_{room_id}.csv'
        with open(fp_out, 'w', newline = '') as f1:
            csvwriter = csv.writer(f1)
            csvwriter.writerow(list(result))
            for row in zip(*list(result.values())):
                csvwriter.writerow(row)
print()

# 5. Export apache system misc results
print('Export apache system misc results', end = ' ')
with iesve.ResultsReader.open(fp_in) as f:
    model_level = 'v'
    variables = [x for x in f.get_variables() if x['model_level'] == model_level] 
    for system_id in [x[1] for x in f.get_apache_systems()]:
        print(system_id, end = ' ')
        result = {variable['display_name']: f.get_apache_system_results(system_id, variable['aps_varname'], variable['display_name'], model_level) for variable in variables}
        result = {k:[None] * 8760 if v is None else v for k,v in result.items()}   
        fp_out = f'{fp_in[:-4]}_apache_system_misc_{system_id}.csv'
        with open(fp_out, 'w', newline = '') as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow(list(result))
            for row in zip(*list(result.values())):
                csvwriter.writerow(row)
print()

# 6. Export apache system energy results
print('Export apache system energy results', end = ' ')
with iesve.ResultsReader.open(fp_in) as f:
    model_level = 'j'
    variables = [x for x in f.get_variables() if x['model_level'] == model_level] 
    for system_id in [x[1] for x in f.get_apache_systems()]:
        print(system_id, end = ' ')
        result = {variable['display_name']: f.get_apache_system_results(system_id, variable['aps_varname'], variable['display_name'], model_level) for variable in variables}
        result = {k:[None] * 8760 if v is None else v for k,v in result.items()}   
        fp_out = f'{fp_in[:-4]}_apache_system_energy_{system_id}.csv'
        with open(fp_out, 'w', newline = '') as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow(list(result))
            for row in zip(*list(result.values())):
                csvwriter.writerow(row)
print()

# 7. Export apache system carbon results
print('Export apache system carbon results', end = ' ')
with iesve.ResultsReader.open(fp_in) as f:
    model_level = 'r'
    variables = [x for x in f.get_variables() if x['model_level'] == model_level] 
    for system_id in [x[1] for x in f.get_apache_systems()]:
        print(system_id, end = ' ')
        result = {variable['display_name']: f.get_apache_system_results(system_id, variable['aps_varname'], variable['display_name'], model_level) for variable in variables}
        result = {k:[None] * 8760 if v is None else v for k,v in result.items()}   
        fp_out = f'{fp_in[:-4]}_apache_system_carbon_{system_id}.csv'
        with open(fp_out, 'w', newline = '') as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow(list(result))
            for row in zip(*list(result.values())):
                csvwriter.writerow(row)
print()

# 8. Export building loads results
print('Export building loads results', end = ' ')
with iesve.ResultsReader.open(fp_in) as f:
    model_level = 'l'
    variables = [x for x in f.get_variables() if x['model_level'] == model_level]  
    result = {variable['display_name']: f.get_results(variable['aps_varname'], variable['display_name'], model_level) for variable in variables}
    result = {k:[None] * 8760 if v is None else v for k,v in result.items()}   
    fp_out = f'{fp_in[:-4]}_building_loads.csv'
    with open(fp_out, 'w', newline = '') as f1:
        csvwriter = csv.writer(f1)
        csvwriter.writerow(list(result))
        for row in zip(*list(result.values())):
            csvwriter.writerow(row)
print()

# 9. Export building energy results
print('Export building energy results', end = ' ')
with iesve.ResultsReader.open(fp_in) as f:
    model_level = 'e'
    variables = [x for x in f.get_variables() if x['model_level'] == model_level]  
    result = {variable['display_name']: f.get_results(variable['aps_varname'], variable['display_name'], model_level) for variable in variables}
    result = {k:[None] * 8760 if v is None else v for k,v in result.items()}   
    fp_out = f'{fp_in[:-4]}_building_energy.csv'
    with open(fp_out, 'w', newline = '') as f1:
        csvwriter = csv.writer(f1)
        csvwriter.writerow(list(result))
        for row in zip(*list(result.values())):
            csvwriter.writerow(row)
print()

# 10. Export building carbon results
print('Export building carbon results', end = ' ')
with iesve.ResultsReader.open(fp_in) as f:
    model_level = 'c'
    variables = [x for x in f.get_variables() if x['model_level'] == model_level]  
    result = {variable['display_name']: f.get_results(variable['aps_varname'], variable['display_name'], model_level) for variable in variables}
    result = {k:[None] * 8760 if v is None else v for k,v in result.items()}   
    fp_out = f'{fp_in[:-4]}_building_carbon.csv'
    with open(fp_out, 'w', newline = '') as f1:
        csvwriter = csv.writer(f1)
        csvwriter.writerow(list(result))
        for row in zip(*list(result.values())):
            csvwriter.writerow(row)
print()

# 11. Export surface_level results
print('Export surface_level results', end = ' ')
with iesve.ResultsReader.open(fp_in) as f:
    model_level = 's'
    variables = [x for x in f.get_variables() if x['model_level'] == model_level]  
    for body in current_project.models[0].get_bodies(False):
        room_id = body.get_room_data().id
        #print('room_id', room_id, end = ' ')
        for surface in body.get_surfaces():
            aps_handle = surface.get_properties()['aps_handle']
            surface_id = surface.get_properties()['id']
            print(surface_id, end = ' ')
            result = {variable['display_name']: f.get_all_surface_results(room_id, aps_handle, variable['aps_varname']) for variable in variables}
            result = {k:[None] * 8760 if v is None else v for k,v in result.items()}   
            fp_out = f'{fp_in[:-4]}_surface_level_{room_id}_{surface_id}.csv'
            with open(fp_out, 'w', newline = '') as f1:
                csvwriter = csv.writer(f1)
                csvwriter.writerow(list(result))
                for row in zip(*list(result.values())):
                    csvwriter.writerow(row)
print()

# 12. Export opening_level results
print('Export opening_level results', end = ' ')
with iesve.ResultsReader.open(fp_in) as f:
    model_level = 'o'
    variables = [x for x in f.get_variables() if x['model_level'] == model_level]  
    for body in current_project.models[0].get_bodies(False):
        room_id = body.get_room_data().id
        #print('room_id', room_id, end = ' ')
        for surface in body.get_surfaces():
            aps_handle = surface.get_properties()['aps_handle']
            surface_id = surface.get_properties()['id']
            #print('surface_id', surface_id, end = ' ')
            surface_index = surface.index
            for opening in surface.get_openings():
                opening_id = opening.get_id()
                print(opening_id, end = ' ')
                opening_index = opening.get_properties()['index']
                result = {variable['display_name']: f.get_all_opening_results(room_id, surface_index, opening_index, variable['aps_varname']) for variable in variables}
                result = {k:[None] * 8760 if v is None else v for k,v in result.items()}   
                fp_out = f'{fp_in[:-4]}_opening_level_{room_id}_{opening_id}.csv'
                with open(fp_out, 'w', newline = '') as f1:
                    csvwriter = csv.writer(f1)
                    csvwriter.writerow(list(result))
                    for row in zip(*list(result.values())):
                        csvwriter.writerow(row)
print()

# 13. Export hvac_node_level results
# -- TO DO IF NEEDED --
# n
# get_hvac_node_results(node_nr, layer_nr = -1, var_name, start_day = -1, end_day = -1)
# -> Numpy array of floats
# Get the results for HVAC Node.  Use layer_nr to specify multiplex layer, or -1 for plant-side node (outside of multiplex).  See variables list for available variables and matching level.  See get_results for start_day and end_day details.
 
# 14. Export hvac_component_level results
# -- TO DO IF NEEDED --
# h
# get_hvac_component_results( component_id, component_type, var_name, start_day = -1, end_day = -1 )
# -> Numpy array of floats
# Get the results for HVAC Component ID + variable.  See variables list for available variables and matching level.  See get_results for start_day and end_day details.
 
print('END')
