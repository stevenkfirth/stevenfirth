print('--- START - export_construction_data.py ---')

import json
from pprint import pprint

import iesve  # Imports the iesve module
project = iesve.VEProject.get_current_project()  # Uses the static method 'get_current_project' of the VEProject class to return a VEProject instance object
models = project.models  # Uses the 'models' property to return a list of the models in the current project
realmodel=models[0] # Get the 'real' model - it's the first in the list
bodies = realmodel.get_bodies(False)  # Get a list of all VEBody instances in the realmodel. The argument False returns all bodies (True returns selected bodies only)
construction_ids=set(construction_id for body in bodies for surface in body.get_surfaces() for construction_id in surface.get_constructions())  # Set of construction ids (strings) used by the surfaces in the model

db = iesve.VECdbDatabase.get_current_database()  # Uses the static method 'get_current_database' of the VECdbDatabase class to return a VECdbDatabase instance object
vecdb_project=db.get_projects()[iesve.project_types.project][0]  # Gets the first 'iesve.project_types.project' construction project in the database.

construction_data={}
for construction_id in construction_ids:  # loop through the construction ids
    d={}
    construction=vecdb_project.get_construction(construction_id,iesve.construction_class.none)  # get the construction instance
    #print([x for x in dir(construction) if not x.startswith('__')])
    d=dict(
        c_factor=construction.c_factor,
        category=construction.category, 
        category_string=iesve.VECdbProject.get_category_string(construction.category),  # get the category string
        f_factor=construction.f_factor,
        get_default_resistances=construction.get_default_resistances(),
        get_g_values=construction.get_g_values(),
        get_layers=[layer.get_id() for layer in construction.get_layers()],
        get_properties=construction.get_properties(),
        get_review_summary_string=construction.get_review_summary_string(),
        get_u_factor={
            'cibse':construction.get_u_factor(iesve.uvalue_types.cibse),
            'iso':construction.get_u_factor(iesve.uvalue_types.iso),
            'ashrae':construction.get_u_factor(iesve.uvalue_types.ashrae),
            't24':construction.get_u_factor(iesve.uvalue_types.t24),
        },
        id=construction.id,
        is_editable=construction.is_editable,
        opaque=construction.opaque,
        reference=construction.reference,
        regulation=construction.regulation,
        regulation_string=str(construction.regulation),
            )
    pprint(d)     
    construction_data[construction_id]=d
    #break
with open('test.json','w') as f:
    json.dump(construction_data,f, indent=4)