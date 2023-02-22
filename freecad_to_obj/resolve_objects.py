from typing import Callable, List

from FreeCAD import Placement

__all__ = ['resolve_objects']

ASSEMBLY_TYPE_IDS = {'App::Part', 'App::Link'}


def resolve_objects(objects: List[object],
                    keep_unresolved: Callable[[
                        object, List[object]], bool] = None,
                    object_name_getter: Callable[[
                        object, List[object], int], str] = lambda obj, path, shape_index: obj.Label,
                    ignore_object: Callable[[
                        object, List[object]], bool] = lambda obj, path: False,
                    export_link_array_elements: bool = False,
                    path: list = [],
                    parent_placement: Placement = None,
                    chain: bool = True) -> dict:
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
                args = _get_resolve_objects_args(obj,
                                                 keep_unresolved,
                                                 object_name_getter,
                                                 ignore_object,
                                                 export_link_array_elements,
                                                 path,
                                                 placement)
                dictionaries = resolve_objects(*args)
                resolved.extend(dictionaries)
            else:
                if stay_unresolved and obj.TypeId == 'App::Link' and obj.LinkTransform:
                    placement = placement * obj.LinkedObject.Placement
                shapes = _get_shapes(
                    obj, placement, export_link_array_elements)
                for shape_index, shape in enumerate(shapes):
                    object_name = object_name_getter(obj, path, shape_index)
                    if type(object_name) != str:
                        raise ValueError(
                            'object_name_getter must return string.')
                    resolved.append({
                        'shape': shape,
                        'name': object_name,
                        'path': path
                    })
    return resolved


def _get_resolve_objects_args(obj,
                              keep_unresolved,
                              object_name_getter,
                              ignore_object,
                              export_link_array_elements,
                              path,
                              placement):
    path_with_obj = path + [obj]
    if obj.TypeId == 'App::Part':
        return [
            obj.Group,
            keep_unresolved,
            object_name_getter,
            ignore_object,
            export_link_array_elements,
            path_with_obj,
            placement,
            True
        ]
    elif obj.TypeId == 'App::Link':
        return [
            [obj.LinkedObject],
            keep_unresolved,
            object_name_getter,
            ignore_object,
            export_link_array_elements,
            path_with_obj,
            placement,
            obj.LinkTransform
        ]


def _get_shapes(obj: object, placement: Placement, export_link_array_elements: bool):
    if obj.TypeId == 'App::Link':
        obj = obj.LinkedObject
    if is_link_array(obj) and export_link_array_elements:
        return [shape.copy(False) for shape in obj.Shape.SubShapes]
    else:
        shape = obj.Shape.copy(False)
        shape.Placement = placement
        return [shape]


def is_link_array(obj: object) -> bool:
    return (
        obj.TypeId == 'Part::FeaturePython' and
        hasattr(obj, 'ArrayType')
    )
