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
from concurrent.futures import ProcessPoolExecutor
from itertools import repeat

from .resolve_objects import resolve_objects

__all__ = ['export']

# https://wiki.freecad.org/Mesh_FromPartShape
default_mesh_settings = {
    'LinearDeflection': 0.1,
    'AngularDeflection': 0.7,
    'Relative': True
}


def export(export_list: List[object],
           object_name_getter: Callable[[
               object, List[object], int], str] = lambda obj, path, shape_index: obj.Label,
           keep_unresolved: Callable[[object, List[object]], bool] = None,
           do_not_export: Callable[[
               object, List[object]], bool] = lambda obj, path: not obj.Visibility,
           export_link_array_elements: bool = False,
           mesh_settings: dict = default_mesh_settings) -> str:
    """
    Transforms a list of objects into a Wavefront .obj file contents.
    """
    lines = []

    # Vertex numbers start from 1 instead of 0
    offsetv = 1
    offsetvn = 1

    resolved_objects = resolve_objects(export_list,
                                       keep_unresolved,
                                       object_name_getter,
                                       do_not_export,
                                       export_link_array_elements)
    shapes = map(lambda o: o['shape'], resolved_objects)
    with ProcessPoolExecutor() as executor:
        mesh_definitions = list(executor.map(_get_mesh_definition, shapes, repeat(mesh_settings)))
    for index, resolved_object in enumerate(resolved_objects):
        shape = resolved_object['shape']
        mesh_definition = mesh_definitions[index]
        print(mesh_definition)
        vlist = mesh_definition['vertexes']
        vnlist = mesh_definition['vertex_normals']
        facets = mesh_definition['facets']
        object_name = resolved_object['name']
        lines.append('o ' + object_name)

        for v in vlist:
            lines.append(f'v {v[0]} {v[1]} {v[2]}')
        for vn in vnlist:
            lines.append(f'vn {vn[0]} {vn[1]} {vn[2]}')
        for i, facet in enumerate(facets):
            f = str(facet[0] + offsetv) + '//' + \
                str(i + offsetvn) + ' ' + \
                str(facet[1] + offsetv) + '//' + \
                str(i + offsetvn) + ' ' + \
                str(facet[2] + offsetv) + '//' + \
                str(i + offsetvn)
            lines.append('f ' + f)

        offsetv += len(vlist)
        offsetvn += len(vnlist)
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


def _get_mesh_definition(shape, mesh_settings: dict = default_mesh_settings) -> dict:
    """
    Return a tuple containing 3 lists:

        1. vertexes
        2. vertex normals
        3. and face indices

    offset with a given amount.
    """
    mesh_definition = {
        'vertexes': [],
        'facets': [],
        'vertex_normals': []
    }
    # Triangulates shapes with curves
    mesh = MeshPart.meshFromShape(Shape=shape, **mesh_settings)
    vertexes, facets = mesh.Topology
    for vertex in vertexes:
        p = Draft.precision()
        vertex = (round(vertex.x, p), round(vertex.y, p), round(vertex.z, p))
        mesh_definition['vertexes'].append(vertex)
    mesh_definition['facets'] = facets
    mesh_definition['vertex_normals'] = list(
        map(lambda f: tuple(f.Normal), mesh.Facets))
    return mesh_definition


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
