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

from typing import Callable, List, Tuple

import Draft
import MeshPart
import Part

from .resolve_objects import resolve_objects

__all__ = ['export']


def export(export_list: List[object],
           object_name_getter: Callable[[
               object, List[object]], str] = lambda obj, path: obj.Label,
           keep_unresolved: Callable[[object, List[object]], bool] = None,
           do_not_export: Callable[[object, List[object]], bool] = lambda obj, path: not obj.Visibility) -> str:
    """
    Transforms a list of objects into a Wavefront .obj file contents.
    """
    lines = []

    # Vertex numbers start from 1 instead of 0
    offsetv = 1
    offsetvn = 1

    resolved_objects = resolve_objects(
        export_list, keep_unresolved, do_not_export)
    for resolved_object in resolved_objects:
        obj = resolved_object['object']
        placement = resolved_object['placement']
        path = resolved_object['path']
        shape = obj.Shape.copy(False)
        shape.Placement = placement

        vlist, vnlist, flist = _get_indices(shape, offsetv, offsetvn)

        offsetv += len(vlist)
        offsetvn += len(vnlist)
        object_name = object_name_getter(obj, path)
        if type(object_name) != str:
            raise ValueError('object_name_getter must return string.')
        lines.append('o ' + object_name)

        for v in vlist:
            lines.append('v ' + v)
        for vn in vnlist:
            lines.append('vn ' + vn)
        for f in flist:
            lines.append('f ' + f)

        wires = get_wires(shape)

        for i, wire in enumerate(wires):
            # TODO: Consider passing in wire_label_delimiter argument.
            lines.append(f'o {object_name}Wire{i}')
            line_segments = []
            for vertex in wire:
                x, y, z = vertex
                lines.append(f'v {x} {y} {z}')
                line_segments.append(str(offsetv))
                offsetv += 1
            lines.append('l ' + ' '.join(line_segments))
    if len(lines) == 0:
        return ''
    return '\n'.join(lines) + '\n'


def _get_indices(shape, offsetv: int, offsetvn: int) -> Tuple[List[str], List[str], List[str]]:
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


def get_wires(shape) -> List[List[Tuple[str, str, str]]]:
    wires = []
    for face in shape.Faces:
        for wire in face.Wires:
            discretized_wire = discretize_wire(wire)
            wire = []
            for vertex in discretized_wire:
                # use strings to avoid 0.00001 written as 1e-05
                # TODO: This uses 5 decimal places of precision,
                #       where we use p = Draft.precision() above.
                #       We should make the precision consistent.
                x = '{:.5f}'.format(vertex.x)
                y = '{:.5f}'.format(vertex.y)
                z = '{:.5f}'.format(vertex.z)
                wire.append((x, y, z))
            wires.append(wire)
    return wires


def discretize_wire(wire: Part.Wire) -> Part.Wire:
    wire_with_sorted_edges = Part.Wire(Part.__sortEdges__(wire.Edges))
    return wire_with_sorted_edges.discretize(QuasiDeflection=0.005)
