import os
import unittest
from pathlib import Path

import FreeCAD as App
import freecad_to_obj
from FreeCAD import Placement, Rotation, Vector


class ExportWithPartPrimitivesTest(unittest.TestCase):
    """
    See Also:
        https://wiki.freecadweb.org/Part_Primitives
    """

    def test_export_with_cube(self):
        document = App.newDocument()
        box = document.addObject('Part::Box', 'Box')
        box.Label = 'Cube'
        document.recompute()
        with open(os.path.join(os.path.dirname(__file__), 'cube.obj')) as f:
            expected = f.read()

        obj_file_contents = freecad_to_obj.export([box])

        self.assertEqual(obj_file_contents, expected)

    def test_export_with_translated_cube(self):
        document = App.newDocument()
        box = document.addObject('Part::Box', 'Box')
        box.Label = 'Cube'
        box.Placement = Placement(
            Vector(10, 0, 0), Rotation(Vector(0, 0, 1), 0))
        document.recompute()
        with open(os.path.join(os.path.dirname(__file__), 'translated_cube.obj')) as f:
            expected = f.read()

        obj_file_contents = freecad_to_obj.export([box])

        self.assertEqual(obj_file_contents, expected)

    def test_export_with_cylinder(self):
        document = App.newDocument()
        cylinder = document.addObject('Part::Cylinder', 'Cylinder')
        cylinder.Label = 'Cylinder'
        document.recompute()
        with open(os.path.join(os.path.dirname(__file__), 'cylinder.obj')) as f:
            expected = f.read()

        obj_file_contents = freecad_to_obj.export([cylinder])

        self.assertEqual(obj_file_contents, expected)

    def test_export_with_torus(self):
        document = App.newDocument()
        torus = document.addObject('Part::Torus', 'Torus')
        torus.Label = 'Torus'
        document.recompute()
        with open(os.path.join(os.path.dirname(__file__), 'torus.obj')) as f:
            expected = f.read()

        obj_file_contents = freecad_to_obj.export([torus])

        self.assertEqual(obj_file_contents, expected)

    def test_export_with_sphere(self):
        document = App.newDocument()
        sphere = document.addObject('Part::Sphere', 'Sphere')
        sphere.Label = 'Sphere'
        document.recompute()
        with open(os.path.join(os.path.dirname(__file__), 'sphere.obj')) as f:
            expected = f.read()

        obj_file_contents = freecad_to_obj.export([sphere])

        self.assertEqual(obj_file_contents, expected)

    def test_export_with_translated_sphere(self):
        document = App.newDocument()
        sphere = document.addObject('Part::Sphere', 'Sphere')
        sphere.Label = 'Sphere'
        sphere.Placement = Placement(
            Vector(10, 0, 0), Rotation(Vector(0, 0, 1), 0))
        document.recompute()
        with open(os.path.join(os.path.dirname(__file__), 'translated_sphere.obj')) as f:
            expected = f.read()

        obj_file_contents = freecad_to_obj.export([sphere])

        self.assertEqual(obj_file_contents, expected)


if __name__ == '__main__':
    unittest.main()
