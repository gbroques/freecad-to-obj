from typing import Callable, List

from FreeCAD import Placement

__all__ = ['resolve_objects']

ASSEMBLY_TYPE_IDS = {'App::Part', 'App::Link'}


def resolve_objects(objects: List[object],
                    keep_unresolved: Callable[[
                        object, List[object]], bool] = None,
                    ignore_object: Callable[[
                        object, List[object]], bool] = lambda obj, path: False,
                    path: list = [],
                    parent_placement: Placement = None,
                    chain: bool = True) -> List[dict]:
    resolved = []
    for obj in objects:
        if not ignore_object(obj, path):
            placement = obj.Placement
            if parent_placement:
                if chain:
                    placement = parent_placement * placement
                else:
                    placement = parent_placement
            stay_unresolved = keep_unresolved and keep_unresolved(obj, path)
            if obj.TypeId in ASSEMBLY_TYPE_IDS and not stay_unresolved:
                args = _get_resolve_objects_args(
                    obj, keep_unresolved, ignore_object, path, placement)
                dictionaries = resolve_objects(*args)
                resolved.extend(dictionaries)
            else:
                if stay_unresolved and obj.TypeId == 'App::Link' and obj.LinkTransform:
                    placement = placement * obj.LinkedObject.Placement
                resolved.append({
                    'object': obj,
                    'placement': placement,
                    'path': path
                })
    return resolved


def _get_resolve_objects_args(obj, keep_unresolved, ignore_object, path, placement):
    path_with_obj = path + [obj]
    if obj.TypeId == 'App::Part':
        return [
            obj.Group,
            keep_unresolved,
            ignore_object,
            path_with_obj,
            placement,
            True
        ]
    elif obj.TypeId == 'App::Link':
        return [
            [obj.LinkedObject],
            keep_unresolved,
            ignore_object,
            path_with_obj,
            placement,
            obj.LinkTransform
        ]
