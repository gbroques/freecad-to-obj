import os
import unittest

import FreeCAD as App
import freecad_to_obj
from FreeCAD import Placement, Rotation, Vector


class FreeCADToObjExportTest(unittest.TestCase):

    def test_export(self):
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

    def test_export_with_translated_part(self):
        document = App.newDocument()
        box = document.addObject('Part::Box', 'Box')
        box.Label = 'Cube'
        part = document.addObject('App::Part', 'Part')
        part.addObject(box)
        part.Placement = Placement(
            Vector(10, 0, 0), Rotation(Vector(0, 0, 1), 0))
        document.recompute()
        with open(os.path.join(os.path.dirname(__file__), 'translated_cube.obj')) as f:
            expected = f.read()

        obj_file_contents = freecad_to_obj.export([part])

        self.assertEqual(obj_file_contents, expected)


if __name__ == '__main__':
    unittest.main()
