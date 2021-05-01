from typing import List, Tuple

from FreeCAD import Placement


def resolve_objects(objects, parent_placement=None, chain=True) -> List[Tuple[object, Placement]]:
    resolved = []
    for obj in objects:
        placement = obj.Placement
        if parent_placement:
            if chain:
                placement = placement * parent_placement
            else:
                placement = parent_placement

        if obj.TypeId == 'App::Part':
            objs = resolve_objects(obj.Group, placement, True)
            resolved.extend(objs)
        elif obj.TypeId == 'App::Link':
            objs = resolve_objects(
                [obj.LinkedObject], placement, obj.LinkTransform)
            resolved.extend(objs)
        else:
            resolved.append((obj, placement))
    return resolved
