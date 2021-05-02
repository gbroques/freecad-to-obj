from typing import Callable, List, Tuple

from FreeCAD import Placement

__all__ = ['resolve_objects']

ASSEMBLY_TYPE_IDS = {'App::Part', 'App::Link'}


def resolve_objects(objects: List[object],
                    keep_unresolved: Callable[[object], bool] = None,
                    parent_placement: Placement = None,
                    chain: bool = True) -> List[Tuple[object, Placement]]:
    resolved = []
    for obj in objects:
        placement = obj.Placement
        if parent_placement:
            if chain:
                placement = parent_placement * placement
            else:
                placement = parent_placement
        stay_unresolved = keep_unresolved and keep_unresolved(obj)
        if obj.TypeId in ASSEMBLY_TYPE_IDS and not stay_unresolved:
            args = _get_resolve_objects_args(
                obj, keep_unresolved, placement)
            objs = resolve_objects(*args)
            resolved.extend(objs)
        else:
            if stay_unresolved and obj.TypeId == 'App::Link' and obj.LinkTransform:
                placement = placement * obj.LinkedObject.Placement
            resolved.append((obj, placement))
    return resolved


def _get_resolve_objects_args(obj, keep_unresolved, placement):
    if obj.TypeId == 'App::Part':
        return [
            obj.Group,
            keep_unresolved,
            placement,
            True
        ]
    elif obj.TypeId == 'App::Link':
        return [
            [obj.LinkedObject],
            keep_unresolved,
            placement,
            obj.LinkTransform
        ]
