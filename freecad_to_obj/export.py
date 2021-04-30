"""
Module to export to Wavefront .obj format.

See:
  https://en.wikipedia.org/wiki/Wavefront_.obj_file

Adapted from:
  https://github.com/FreeCAD/FreeCAD/blob/0.19.1/src/Mod/Arch/importOBJ.py#L149-L273

Adapting this code is somewhat of a hack, but in the future we will use glTF instead. 

Modifications:
  * Use object Label instead of Name for object name.
  * Remove mtl or materials generation.
  * Return .obj file contents as string instead of writing to a file.
  * Removed support of experimental high-resolution Arch feature.
    * See: https://forum.freecadweb.org/viewtopic.php?t=21144
  * Removed any code paths requiring FreeCAD's GUI to be active.
    * This script is meant to be ran from a server environment only.
  * Remove support for meshes and "Mesh Feature" objects.
    * See: https://wiki.freecadweb.org/Mesh_Feature
"""

from typing import List, Tuple

import Draft
import FreeCAD as App
import MeshPart

__all__ = ['export']


def export(export_list) -> str:
    """
    Transforms a list of objects into a Wavefront .obj file contents.
    """
    lines = []

    offsetv = 1
    offsetvn = 1

    objects = _ungroup_objects(export_list)
    for obj in objects:
        if obj.isDerivedFrom('Part::Feature') or obj.isDerivedFrom('App::Link'):
            vlist, vnlist, flist = _get_indices(obj, offsetv, offsetvn)

            offsetv += len(vlist)
            offsetvn += len(vnlist)
            lines.append('o ' + obj.Label)

            for v in vlist:
                lines.append('v ' + v)
            for vn in vnlist:
                lines.append('vn ' + vn)
            for f in flist:
                lines.append('f ' + f)
    return '\n'.join(lines) + '\n'


def _get_indices(obj, offsetv: int, offsetvn: int) -> Tuple[List[str], List[str], List[str]]:
    """
    Return a tuple containing 3 lists:

        1. vertexes
        2. vertex normals
        3. and face indices

    offset with a given amount.
    """
    vlist = []
    vnlist = []
    flist = []

    shape = obj.Shape.copy(False)

    # Triangulates shapes with curves
    mesh = MeshPart.meshFromShape(
        Shape=shape, LinearDeflection=0.1, AngularDeflection=0.7, Relative=True)
    for v in mesh.Topology[0]:
        p = Draft.precision()
        vlist.append(str(round(v[0], p)) + ' ' +
                     str(round(v[1], p)) + ' ' +
                     str(round(v[2], p)))

    for vn in mesh.Facets:
        vnlist.append(str(vn.Normal[0]) + ' ' +
                      str(vn.Normal[1]) + ' ' +
                      str(vn.Normal[2]))

    for i, vn in enumerate(mesh.Topology[1]):
        flist.append(str(vn[0] + offsetv) + '//' +
                     str(i + offsetvn) + ' ' +
                     str(vn[1] + offsetv) + '//' +
                     str(i + offsetvn) + ' ' +
                     str(vn[2] + offsetv) + '//' +
                     str(i + offsetvn))

    return vlist, vnlist, flist


def _ungroup_objects(objects, placement_strategy=None) -> list:
    ungrouped = []
    for obj in objects:
        if placement_strategy:
            obj.Placement = placement_strategy(obj.Placement)

        if obj.TypeId == 'App::Part':
            def link_placement_strategy(child_placement):
                return child_placement * obj.Placement
            objs = _ungroup_objects(obj.Group, link_placement_strategy)
            ungrouped.extend(objs)
        elif obj.TypeId == 'App::Link':
            def link_placement_strategy(child_placement):
                if obj.LinkTransform:
                    return child_placement * obj.Placement
                else:
                    return obj.LinkPlacement
            objs = _ungroup_objects(
                [obj.LinkedObject], link_placement_strategy)
            ungrouped.extend(objs)
        else:
            ungrouped.append(obj)
    return ungrouped
