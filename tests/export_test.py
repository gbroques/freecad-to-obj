import os
import unittest
from pathlib import Path

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

    def test_export_with_translated_link(self):
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

    def test_export_with_link_transform_true(self):
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

    def test_export_with_cylinder(self):
        document = App.newDocument()
        cylinder = document.addObject('Part::Cylinder','Cylinder')
        cylinder.Label = 'Cylinder'
        document.recompute()
        with open(os.path.join(os.path.dirname(__file__), 'cylinder.obj')) as f:
            expected = f.read()

        obj_file_contents = freecad_to_obj.export([cylinder])

        self.assertEqual(obj_file_contents, expected)

    def test_export_with_torus(self):
        document = App.newDocument()
        torus = document.addObject('Part::Torus','Torus')
        torus.Label = 'Torus'
        document.recompute()
        with open(os.path.join(os.path.dirname(__file__), 'torus.obj')) as f:
            expected = f.read()

        obj_file_contents = freecad_to_obj.export([torus])

        self.assertEqual(obj_file_contents, expected)

    def test_export_with_sphere(self):
        document = App.newDocument()
        sphere = document.addObject('Part::Sphere','Sphere')
        sphere.Label = 'Sphere'
        document.recompute()
        with open(os.path.join(os.path.dirname(__file__), 'sphere.obj')) as f:
            expected = f.read()

        obj_file_contents = freecad_to_obj.export([sphere])

        self.assertEqual(obj_file_contents, expected)

    def test_export_with_sphere_link(self):
        test_package_path = Path(__file__).parent

        sphere_document = App.newDocument('Sphere')
        sphere = sphere_document.addObject('Part::Sphere','Sphere')
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


if __name__ == '__main__':
    unittest.main()
