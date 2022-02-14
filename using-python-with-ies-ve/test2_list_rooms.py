# test2_list_rooms.py

import iesve
project = iesve.VEProject.get_current_project()
models = project.models
realmodel = models[0]
bodies = realmodel.get_bodies(False)
rooms = [body for body in bodies if body.subtype==iesve.VEBody_subtype.room]
for room in rooms:
    print(room.id,room.name)
