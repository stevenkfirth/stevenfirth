print('--- START - generate_construction_tables.py ---')

import iesve  # Imports the iesve module
project = iesve.VEProject.get_current_project()  # Uses the static method 'get_current_project' of the VEProject class to return a VEProject instance object
models = project.models  # Uses the 'models' property to return a list of the models in the current project
realmodel=models[0] # Get the 'real' model - it's the first in the list
bodies = realmodel.get_bodies(False)  # Get a list of all VEBody instances in the realmodel. The argument False returns all bodies (True returns selected bodies only)
construction_ids=set(construction_id for body in bodies for surface in body.get_surfaces() for construction_id in surface.get_constructions())  # Set of construction ids (strings) used by the surfaces in the model

db = iesve.VECdbDatabase.get_current_database()  # Uses the static method 'get_current_database' of the VECdbDatabase class to return a VECdbDatabase instance object
vecdb_project=db.get_projects()[iesve.project_types.project][0]  # Gets the first 'iesve.project_types.project' construction project in the database.

import csv  # Imports the built-in csv module, used to create the csv files

# --- Create the Summary Construction table ---
print('--- creating Summary Construction table ---')
with open('Summary_construction_table.csv','w', newline='') as f:  # to create a new summary csv file
    writer=csv.writer(f)
    writer.writerow(['Construction category','U-value (W/m2K)','Thickness (m)','Layers (outside to inside)'])  # write the headers of the csv file
    for construction_id in construction_ids:  # loop through the construction ids
        construction=vecdb_project.get_construction(construction_id,iesve.construction_class.none)  # get the construction instance
        category_string=iesve.VECdbProject.get_category_string(construction.category)  # get the category string
        u_value=construction.get_u_factor(iesve.uvalue_types.cibse)  # get the u-value
        construction_thickness=sum([layer.get_properties()['thickness'] for layer in construction.get_layers()])  # get the total thickness of the construction
        layers_description=[]  #  a list with a short description for each layer, populated below
        for layer in construction.get_layers():  # loop through the layers of the construction
            material=layer.get_material(construction.opaque)  # get the material of the layer
            thickness=layer.get_properties()['thickness']  # get the thickness of the layer
            if not material is None:  # i.e. not a cavity
                layers_description.append('%s (%0.1fmm)' % (material.get_properties()['description'], thickness*1000))  # adds a layer description
            else:  # i.e. a cavity
                layers_description.append('Cavity (%0.1fmm)' % (thickness*1000))  # adds a layer description
        writer.writerow([category_string,'%0.2f' % u_value, '%0.3f' % construction_thickness, ', '.join(layers_description)])  # write a row of data in the csv file
for line in open('Summary_construction_table.csv'): print(line, end='')  # prints out the csv file in the 'Output' pane
    
# --- Create the Opaque Materials table ---
print('--- creating Opaque Materials table ---')
with open('Opaque_materials_table.csv','w', newline='') as f:  # to create a new opaque materials csv file
    writer=csv.writer(f)
    writer.writerow(['Material','Thermal conductivity (W/mK)','Density (kg/m3)','Specific heat capacity (J/kgK)'])  # write the headers of the csv file
    materials_dict={}
    for construction_id in construction_ids:  # loop through the construction ids
        construction=vecdb_project.get_construction(construction_id,iesve.construction_class.none)  # get the construction instance
        if construction.opaque:
            for layer in construction.get_layers():  # loop through the layers of the construction
                material=layer.get_material(True)  # opaque constructions only
                if not material is None:  # i.e. not a cavity
                    materials_dict[material.get_properties()['description']]=material.get_properties()
    for material_description in sorted(materials_dict):
        material_properties=materials_dict[material_description]
        writer.writerow([material_description,
                         '{:.2f}'.format(material_properties['conductivity']),
                         '{:,.0f}'.format(material_properties['density']),
                         '{:,.0f}'.format(material_properties['specific_heat_capacity']),
                         ])
for line in open('Opaque_materials_table.csv'): print(line, end='')  # prints out the csv file in the 'Output' pane

# --- Create the Glazing Materials table ---
print('--- creating Glazing Materials table ---')
with open('Glazing_materials_table.csv','w', newline='') as f:  # to create a new opaque materials csv file
    writer=csv.writer(f)
    writer.writerow(['Material','Thermal conductivity (W/mK)','Specific heat capacity (J/kgK)','Transmittance'])  # write the headers of the csv file
    materials_dict={}
    for construction_id in construction_ids:  # loop through the construction ids
        construction=vecdb_project.get_construction(construction_id,iesve.construction_class.none)  # get the construction instance
        if not construction.opaque:
            for layer in construction.get_layers():  # loop through the layers of the construction
                material=layer.get_material(False)  # non-opaque constructions
                if not material is None:  # i.e. not a cavity
                    materials_dict[material.get_properties()['description']]=material.get_properties()
    for material_description in sorted(materials_dict):
        material_properties=materials_dict[material_description]
        print(material_properties)
        writer.writerow([material_description,
                         '{:.2f}'.format(material_properties['conductivity']),
                         '{:,.2f}'.format(material_properties['specific_heat_capacity']),
                         '{:,.2f}'.format(material_properties['transmittance']),
                         ])
for line in open('Glazing_materials_table.csv'): print(line, end='')  # prints out the csv file in the 'Output' pane
    
    
    
    
    
    
    
    