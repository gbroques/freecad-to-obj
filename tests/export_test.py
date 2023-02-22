import os
import unittest
from pathlib import Path
from typing import List

import FreeCAD as App
import freecad_to_obj
import Part
import Sketcher
from FreeCAD import Placement, Rotation, Vector


class ExportTest(unittest.TestCase):

    def test_export_with_translated_part_containing_translated_primitive(self):
        document = App.newDocument()
        box = document.addObject('Part::Box', 'Box')
        box.Label = 'Cube'
        box.Placement = Placement(
            Vector(5, 0, 0), Rotation(Vector(0, 0, 1), 0))

        part = document.addObject('App::Part', 'Part')
        part.addObject(box)
        part.Placement = Placement(
            Vector(5, 0, 0), Rotation(Vector(0, 0, 1), 0))
        document.recompute()

        with open(os.path.join(os.path.dirname(__file__), 'translated_cube.obj')) as f:
            expected = f.read()

        obj_file_contents = freecad_to_obj.export([part])

        self.assertEqual(obj_file_contents, expected)

    def test_export_with_translated_part_containing_primitive(self):
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

    def test_export_with_translated_link_to_primitive(self):
        test_package_path = Path(__file__).parent

        cube_document = App.newDocument('Cube')
        box = cube_document.addObject('Part::Box', 'Box')
        box.Label = 'Cube'

        cube_document_path = test_package_path.joinpath('Cube.FCStd')
        cube_document.saveAs(str(cube_document_path))

        link_document = App.newDocument('CubeLink')
        link_document_path = test_package_path.joinpath('LinkCube.FCStd')
        link_document.saveAs(str(link_document_path))
        link = link_document.addObject('App::Link', 'Link')
        link.setLink(box)
        link.Label = box.Label

        link.Placement = Placement(
            Vector(10, 0, 0), Rotation(Vector(0, 0, 1), 0))

        link_document.recompute()

        with open(os.path.join(os.path.dirname(__file__), 'translated_cube.obj')) as f:
            expected = f.read()

        obj_file_contents = freecad_to_obj.export([link])

        self.assertEqual(obj_file_contents, expected)

        cube_document_path.unlink()
        link_document_path.unlink()

    def test_export_with_link_to_translated_primitive(self):
        test_package_path = Path(__file__).parent

        cube_document = App.newDocument('Cube')
        box = cube_document.addObject('Part::Box', 'Box')
        box.Label = 'Cube'
        box.Placement = Placement(
            Vector(10, 0, 0), Rotation(Vector(0, 0, 1), 0))

        cube_document_path = test_package_path.joinpath('Cube.FCStd')
        cube_document.saveAs(str(cube_document_path))

        link_document = App.newDocument('CubeLink')
        link_document_path = test_package_path.joinpath('LinkCube.FCStd')
        link_document.saveAs(str(link_document_path))
        link = link_document.addObject('App::Link', 'Link')
        link.setLink(box)
        link.Label = box.Label
        link.LinkTransform = False

        link_document.recompute()

        with open(os.path.join(os.path.dirname(__file__), 'cube.obj')) as f:
            expected = f.read()

        obj_file_contents = freecad_to_obj.export([link])

        self.assertEqual(obj_file_contents, expected)

        cube_document_path.unlink()
        link_document_path.unlink()

    def test_export_with_link_to_translated_primitive_and_link_transform_true(self):
        test_package_path = Path(__file__).parent

        cube_document = App.newDocument('Cube')
        box = cube_document.addObject('Part::Box', 'Box')
        box.Label = 'Cube'
        box.Placement = Placement(
            Vector(10, 0, 0), Rotation(Vector(0, 0, 1), 0))
        cube_document.recompute()

        cube_document_path = test_package_path.joinpath('Cube.FCStd')
        cube_document.saveAs(str(cube_document_path))

        link_document = App.newDocument('Link')
        link_document_path = test_package_path.joinpath('Link.FCStd')
        link_document.saveAs(str(link_document_path))
        link = link_document.addObject('App::Link', 'Link')
        link.setLink(box)
        link.Label = box.Label
        link.LinkTransform = True

        link_document.recompute()

        with open(os.path.join(os.path.dirname(__file__), 'translated_cube.obj')) as f:
            expected = f.read()

        obj_file_contents = freecad_to_obj.export([link])

        self.assertEqual(obj_file_contents, expected)

        cube_document_path.unlink()
        link_document_path.unlink()

    def test_export_with_translated_link_to_translated_primitive_and_link_transform_true(self):
        test_package_path = Path(__file__).parent

        cube_document = App.newDocument('Cube')
        box = cube_document.addObject('Part::Box', 'Box')
        box.Label = 'Cube'
        box.Placement = Placement(
            Vector(5, 0, 0), Rotation(Vector(0, 0, 1), 0))
        cube_document.recompute()

        cube_document_path = test_package_path.joinpath('Cube.FCStd')
        cube_document.saveAs(str(cube_document_path))

        link_document = App.newDocument('Link')
        link_document_path = test_package_path.joinpath('Link.FCStd')
        link_document.saveAs(str(link_document_path))
        link = link_document.addObject('App::Link', 'Link')
        link.setLink(box)
        link.Label = box.Label
        link.LinkTransform = True
        link.Placement = Placement(
            Vector(5, 0, 0), Rotation(Vector(0, 0, 1), 0))

        link_document.recompute()

        with open(os.path.join(os.path.dirname(__file__), 'translated_cube.obj')) as f:
            expected = f.read()

        obj_file_contents = freecad_to_obj.export([link])

        self.assertEqual(obj_file_contents, expected)

        cube_document_path.unlink()
        link_document_path.unlink()

    def test_export_with_link_to_sphere(self):
        test_package_path = Path(__file__).parent

        sphere_document = App.newDocument('Sphere')
        sphere = sphere_document.addObject('Part::Sphere', 'Sphere')
        sphere.Label = 'Sphere'
        sphere_document_path = test_package_path.joinpath('Sphere.FCStd')
        sphere_document.saveAs(str(sphere_document_path))

        link_document = App.newDocument('Link')
        link_document_path = test_package_path.joinpath('Link.FCStd')
        link_document.saveAs(str(link_document_path))
        link = link_document.addObject('App::Link', 'Link')
        link.setLink(sphere)
        link.Label = sphere.Label

        link_document.recompute()

        with open(os.path.join(os.path.dirname(__file__), 'sphere.obj')) as f:
            expected = f.read()

        obj_file_contents = freecad_to_obj.export([link])

        self.assertEqual(obj_file_contents, expected)

        sphere_document_path.unlink()
        link_document_path.unlink()

    def test_export_with_sphere_link_transform_true(self):
        test_package_path = Path(__file__).parent

        sphere_document = App.newDocument('Sphere')
        sphere = sphere_document.addObject('Part::Sphere', 'Sphere')
        sphere.Label = 'Sphere'
        sphere.Placement = Placement(
            Vector(10, 0, 0), Rotation(Vector(0, 0, 1), 0))
        sphere_document.recompute()

        sphere_document_path = test_package_path.joinpath('Sphere.FCStd')
        sphere_document.saveAs(str(sphere_document_path))

        link_document = App.newDocument('Link')
        link_document_path = test_package_path.joinpath('Link.FCStd')
        link_document.saveAs(str(link_document_path))
        link = link_document.addObject('App::Link', 'Link')
        link.setLink(sphere)
        link.Label = sphere.Label
        link.LinkTransform = True

        link_document.recompute()

        with open(os.path.join(os.path.dirname(__file__), 'translated_sphere.obj')) as f:
            expected = f.read()

        obj_file_contents = freecad_to_obj.export([link])

        self.assertEqual(obj_file_contents, expected)

        sphere_document_path.unlink()
        link_document_path.unlink()

    def test_export_with_part_design_body(self):
        test_package_path = Path(__file__).parent

        document = App.newDocument('PartDesign')
        body = document.addObject('PartDesign::Body', 'Body')
        sketch = body.newObject('Sketcher::SketchObject', 'Sketch')
        sketch.Support = (document.getObject('XY_Plane'), [''])
        sketch.MapMode = 'FlatFace'
        sketch.addGeometry(Part.Circle(App.Vector(0, 0, 0),
                           App.Vector(0, 0, 1), 10), False)
        sketch.addConstraint(Sketcher.Constraint('Coincident', 0, 3, -1, 1))

        pad = body.newObject('PartDesign::Pad', 'Pad')
        pad.Profile = sketch
        pad.Length = 10.0
        document.recompute()

        with open(os.path.join(os.path.dirname(__file__), 'body.obj')) as f:
            expected = f.read()

        obj_file_contents = freecad_to_obj.export([body])

        self.assertEqual(obj_file_contents, expected)

    def test_export_with_translated_part_containing_link_to_primitive(self):
        test_package_path = Path(__file__).parent

        cube_document = App.newDocument('Cube')
        box = cube_document.addObject('Part::Box', 'Box')
        box.Label = 'Cube'

        cube_document_path = test_package_path.joinpath('Cube.FCStd')
        cube_document.saveAs(str(cube_document_path))

        part_document = App.newDocument('Part')
        part_document_path = test_package_path.joinpath('Part.FCStd')
        part_document.saveAs(str(part_document_path))
        box_link = part_document.addObject('App::Link', 'Link')
        box_link.setLink(box)
        box_link.Label = box.Label

        part = part_document.addObject('App::Part', 'Part')
        part.addObject(box_link)
        part.Placement = Placement(
            Vector(10, 0, 0), Rotation(Vector(0, 0, 1), 0))
        part_document.recompute()

        with open(os.path.join(os.path.dirname(__file__), 'translated_cube.obj')) as f:
            expected = f.read()

        obj_file_contents = freecad_to_obj.export([part])

        self.assertEqual(obj_file_contents, expected)

        cube_document_path.unlink()
        part_document_path.unlink()

    def test_export_with_translated_part_containing_translated_link_to_primitive(self):
        test_package_path = Path(__file__).parent

        cube_document = App.newDocument('Cube')
        box = cube_document.addObject('Part::Box', 'Box')
        box.Label = 'Cube'

        cube_document_path = test_package_path.joinpath('Cube.FCStd')
        cube_document.saveAs(str(cube_document_path))

        part_document = App.newDocument('Part')
        part_document_path = test_package_path.joinpath('Part.FCStd')
        part_document.saveAs(str(part_document_path))
        box_link = part_document.addObject('App::Link', 'Link')
        box_link.setLink(box)
        box_link.Label = box.Label
        box_link.LinkPlacement = Placement(
            Vector(5, 0, 0), Rotation(Vector(0, 0, 1), 0))

        part = part_document.addObject('App::Part', 'Part')
        part.addObject(box_link)
        part.Placement = Placement(
            Vector(5, 0, 0), Rotation(Vector(0, 0, 1), 0))
        part_document.recompute()

        with open(os.path.join(os.path.dirname(__file__), 'translated_cube.obj')) as f:
            expected = f.read()

        obj_file_contents = freecad_to_obj.export([part])

        self.assertEqual(obj_file_contents, expected)

        cube_document_path.unlink()
        part_document_path.unlink()

    def test_export_with_part_containing_translated_link_to_translated_primitive(self):
        test_package_path = Path(__file__).parent

        cube_document = App.newDocument('Cube')
        box = cube_document.addObject('Part::Box', 'Box')
        box.Label = 'Cube'
        box.Placement = Placement(
            Vector(10, 0, 0), Rotation(Vector(0, 0, 1), 0))

        cube_document_path = test_package_path.joinpath('Cube.FCStd')
        cube_document.saveAs(str(cube_document_path))

        part_document = App.newDocument('Part')
        part_document_path = test_package_path.joinpath('Part.FCStd')
        part_document.saveAs(str(part_document_path))
        box_link = part_document.addObject('App::Link', 'Link')
        box_link.setLink(box)
        box_link.Label = box.Label
        box_link.LinkPlacement = Placement(
            Vector(10, 0, 0), Rotation(Vector(0, 0, 1), 0))

        part = part_document.addObject('App::Part', 'Part')
        part.addObject(box_link)
        part_document.recompute()

        with open(os.path.join(os.path.dirname(__file__), 'translated_cube.obj')) as f:
            expected = f.read()

        obj_file_contents = freecad_to_obj.export([part])

        self.assertEqual(obj_file_contents, expected)

        cube_document_path.unlink()
        part_document_path.unlink()

    def test_export_with_translated_link_to_part_containing_link_to_primitive(self):
        test_package_path = Path(__file__).parent

        cube_document = App.newDocument('Cube')
        box = cube_document.addObject('Part::Box', 'Box')
        box.Label = 'Cube'

        cube_document_path = test_package_path.joinpath('Cube.FCStd')
        cube_document.saveAs(str(cube_document_path))

        part_document = App.newDocument('Part')
        part_document_path = test_package_path.joinpath('Part.FCStd')
        part_document.saveAs(str(part_document_path))

        box_link = part_document.addObject('App::Link', 'Link')
        box_link.setLink(box)
        box_link.Label = box.Label

        part = part_document.addObject('App::Part', 'Part')
        part.addObject(box_link)
        part_document.recompute()

        part_link_document = App.newDocument('PartLink')
        part_link_document_path = test_package_path.joinpath('PartLink.FCStd')
        part_link_document.saveAs(str(part_link_document_path))

        part_link = part_link_document.addObject('App::Link', 'Link')
        part_link.setLink(part)
        part_link.Label = part.Label
        part_link.Placement = Placement(
            Vector(10, 0, 0), Rotation(Vector(0, 0, 1), 0))
        part_link_document.recompute()

        with open(os.path.join(os.path.dirname(__file__), 'translated_cube.obj')) as f:
            expected = f.read()

        obj_file_contents = freecad_to_obj.export([part_link])

        self.assertEqual(obj_file_contents, expected)

        cube_document_path.unlink()
        part_document_path.unlink()
        part_link_document_path.unlink()

    def test_export_with_keep_unresolved_part_containing_primitive(self):
        document = App.newDocument()
        box = document.addObject('Part::Box', 'Box')
        box.Label = 'Cube'
        box.Placement = Placement(
            Vector(5, 0, 0), Rotation(Vector(0, 0, 1), 0))

        part = document.addObject('App::Part', 'Part')
        part.Label = 'Part'
        part.addObject(box)
        part.Placement = Placement(
            Vector(5, 0, 0), Rotation(Vector(0, 0, 1), 0))
        document.recompute()

        obj_filename = 'translated_part_containing_cube.obj'
        with open(os.path.join(os.path.dirname(__file__), obj_filename)) as f:
            expected = f.read()

        def keep_unresolved(obj: object, path: List[object]) -> bool:
            return obj.Name == 'Part'

        obj_file_contents = freecad_to_obj.export(
            [part], keep_unresolved=keep_unresolved)

        self.assertEqual(obj_file_contents, expected)

    def test_export_with_keep_unresolved_link_to_primitive(self):
        document = App.newDocument()
        box = document.addObject('Part::Box', 'Box')
        box.Label = 'Cube'
        box.Placement = Placement(
            Vector(5, 0, 0), Rotation(Vector(0, 0, 1), 0))

        link = document.addObject('App::Link', 'Link')
        link.Label = 'CubeLink'
        link.setLink(box)
        link.Placement = Placement(
            Vector(10, 0, 0), Rotation(Vector(0, 0, 1), 0))
        document.recompute()

        obj_filename = 'link_to_translated_cube.obj'
        with open(os.path.join(os.path.dirname(__file__), obj_filename)) as f:
            expected = f.read()

        def keep_unresolved(obj: object, path: List[object]) -> bool:
            return obj.Label == 'CubeLink'

        obj_file_contents = freecad_to_obj.export(
            [link], keep_unresolved=keep_unresolved)

        self.assertEqual(obj_file_contents, expected)

    def test_export_with_keep_unresolved_transform_link_to_primitive(self):
        document = App.newDocument()
        box = document.addObject('Part::Box', 'Box')
        box.Label = 'Cube'
        box.Placement = Placement(
            Vector(5, 0, 0), Rotation(Vector(0, 0, 1), 0))

        link = document.addObject('App::Link', 'Link')
        link.Label = 'CubeLink'
        link.setLink(box)
        link.Placement = Placement(
            Vector(5, 0, 0), Rotation(Vector(0, 0, 1), 0))
        link.LinkTransform = True
        document.recompute()

        obj_filename = 'link_to_translated_cube.obj'
        with open(os.path.join(os.path.dirname(__file__), obj_filename)) as f:
            expected = f.read()

        def keep_unresolved(obj: object, path: List[object]) -> bool:
            return obj.Label == 'CubeLink'

        obj_file_contents = freecad_to_obj.export(
            [link], keep_unresolved=keep_unresolved)

        self.assertEqual(obj_file_contents, expected)

    def test_export_with_object_name_getter(self):
        document = App.newDocument()
        box = document.addObject('Part::Box', 'CubeLink')
        box.Label = 'Cube'
        box.Placement = Placement(
            Vector(10, 0, 0), Rotation(Vector(0, 0, 1), 0))
        document.recompute()

        obj_filename = 'link_to_translated_cube.obj'
        with open(os.path.join(os.path.dirname(__file__), obj_filename)) as f:
            expected = f.read()

        def object_name_getter(obj: object, path: List[object], shape_index: int) -> str:
            return obj.Name

        obj_file_contents = freecad_to_obj.export(
            [box], object_name_getter=object_name_getter)

        self.assertEqual(obj_file_contents, expected)

    def test_export_with_object_name_getter_not_returning_string_raises_value_error(self):
        document = App.newDocument()
        box = document.addObject('Part::Box', 'Box')
        document.recompute()

        def object_name_getter(obj: object, path: List[object], shape_index: int) -> str:
            return obj.Placement
        with self.assertRaises(ValueError) as cm:
            obj_file_contents = freecad_to_obj.export(
                [box], object_name_getter=object_name_getter)

        self.assertEqual(str(cm.exception),
                         'object_name_getter must return string.')

    def test_export_with_do_not_export(self):
        document = App.newDocument()
        box = document.addObject('Part::Box', 'Cube')
        box.Label = 'Cube'
        document.recompute()

        def do_not_export(obj: object, path: List[object]) -> str:
            return True

        obj_file_contents = freecad_to_obj.export(
            [box], do_not_export=do_not_export)

        self.assertEqual(obj_file_contents, '')

    def test_export_with_invisible_object(self):
        document = App.newDocument()
        box = document.addObject('Part::Box', 'Cube')
        box.Label = 'Cube'
        box.Visibility = False
        document.recompute()

        obj_file_contents = freecad_to_obj.export([box])

        self.assertEqual(obj_file_contents, '')


if __name__ == '__main__':
    unittest.main()
