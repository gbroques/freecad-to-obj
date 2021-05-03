import unittest
from typing import List

import FreeCAD as App
from FreeCAD import Placement, Rotation, Vector
from freecad_to_obj.resolve_objects import resolve_objects

from tests.assembler import Assembler


class ResolveObjectsTest(unittest.TestCase):

    def test_resolve_objects_with_shape(self):
        shape = (Assembler()
                 .shape('Part::Box', 'Box', Placement(Vector(10, 0, 0), Rotation()))
                 .assemble())

        resolved_objects = resolve_objects([shape])

        self.assertEqual(len(resolved_objects), 1)

        resolved_object = resolved_objects[0]
        resolved_shape = resolved_object['object']
        placement = resolved_object['placement']
        path = resolved_object['path']

        self.assertEqual(resolved_shape.TypeId, 'Part::Box')
        self.assertEqual(resolved_shape.Name, 'Box')
        self.assertPlacementEqual(placement, Placement(
            Vector(10, 0, 0), Rotation()))
        self.assertEqual(len(path), 0)

    def test_resolve_objects_with_part_containing_shape(self):
        part = (Assembler()
                .part_containing(Placement(Vector(5, 0, 0), Rotation()))
                .shape('Part::Box', 'Box', Placement(Vector(5, 0, 0), Rotation()))
                .assemble())

        resolved_objects = resolve_objects([part])

        self.assertEqual(len(resolved_objects), 1)

        resolved_object = resolved_objects[0]
        resolved_shape = resolved_object['object']
        placement = resolved_object['placement']
        path = resolved_object['path']

        self.assertEqual(resolved_shape.TypeId, 'Part::Box')
        self.assertEqual(resolved_shape.Name, 'Box')
        self.assertPlacementEqual(placement, Placement(
            Vector(10, 0, 0), Rotation()))
        self.assertEqual(len(path), 1)
        self.assertEqual(path[0].TypeId, 'App::Part')

    def test_resolve_objects_with_link_to_shape(self):
        link = (Assembler()
                .link_to(Placement(Vector(10, 0, 0), Rotation()))
                .shape('Part::Box', 'Box', Placement(Vector(5, 0, 0), Rotation()))
                .assemble())

        resolved_objects = resolve_objects([link])

        self.assertEqual(len(resolved_objects), 1)

        resolved_object = resolved_objects[0]
        resolved_shape = resolved_object['object']
        placement = resolved_object['placement']
        path = resolved_object['path']

        self.assertEqual(resolved_shape.TypeId, 'Part::Box')
        self.assertEqual(resolved_shape.Name, 'Box')
        self.assertPlacementEqual(placement, Placement(
            Vector(10, 0, 0), Rotation()))
        self.assertEqual(len(path), 1)
        self.assertEqual(path[0].TypeId, 'App::Link')

    def test_resolve_objects_with_transform_link_to_shape(self):
        transform_link = (Assembler()
                          .transform_link_to(Placement(Vector(10, 0, 0), Rotation()))
                          .shape('Part::Box', 'Box', Placement(Vector(5, 0, 0), Rotation()))
                          .assemble())

        resolved_objects = resolve_objects([transform_link])

        self.assertEqual(len(resolved_objects), 1)

        resolved_object = resolved_objects[0]
        resolved_shape = resolved_object['object']
        placement = resolved_object['placement']
        path = resolved_object['path']

        self.assertEqual(resolved_shape.TypeId, 'Part::Box')
        self.assertEqual(resolved_shape.Name, 'Box')
        self.assertPlacementEqual(placement, Placement(
            Vector(15, 0, 0), Rotation()))
        self.assertEqual(len(path), 1)
        self.assertEqual(path[0].TypeId, 'App::Link')
        self.assertEqual(path[0].LinkTransform, True)

    def test_resolve_objects_with_part_containing_part_containing_shape(self):
        part = (Assembler()
                .part_containing(Placement(Vector(5, 0, 0), Rotation()))
                .part_containing(Placement(Vector(5, 0, 0), Rotation()))
                .shape('Part::Box', 'Box', Placement(Vector(5, 0, 0), Rotation()))
                .assemble())

        resolved_objects = resolve_objects([part])

        self.assertEqual(len(resolved_objects), 1)

        resolved_object = resolved_objects[0]
        resolved_shape = resolved_object['object']
        placement = resolved_object['placement']
        path = resolved_object['path']

        self.assertEqual(resolved_shape.TypeId, 'Part::Box')
        self.assertEqual(resolved_shape.Name, 'Box')
        self.assertPlacementEqual(placement, Placement(
            Vector(15, 0, 0), Rotation()))
        self.assertEqual(len(path), 2)
        self.assertEqual(path[0].TypeId, 'App::Part')
        self.assertEqual(path[1].TypeId, 'App::Part')

    def test_resolve_objects_with_link_to_part_containing_shape(self):
        link = (Assembler()
                .link_to(Placement(Vector(10, 0, 0), Rotation()))
                .part_containing(Placement(Vector(100, 0, 0), Rotation()))
                .shape('Part::Box', 'Box', Placement(Vector(3, 0, 0), Rotation()))
                .assemble())

        resolved_objects = resolve_objects([link])

        self.assertEqual(len(resolved_objects), 1)

        resolved_object = resolved_objects[0]
        resolved_shape = resolved_object['object']
        placement = resolved_object['placement']
        path = resolved_object['path']

        self.assertEqual(resolved_shape.TypeId, 'Part::Box')
        self.assertEqual(resolved_shape.Name, 'Box')
        self.assertPlacementEqual(placement, Placement(
            Vector(13, 0, 0), Rotation()))
        self.assertEqual(len(path), 2)
        self.assertEqual(path[0].TypeId, 'App::Link')
        self.assertEqual(path[1].TypeId, 'App::Part')

    def test_resolve_objects_with_transform_link_to_part_containing_shape(self):
        transform_link = (Assembler()
                          .transform_link_to(Placement(Vector(5, 0, 0), Rotation()))
                          .part_containing(Placement(Vector(5, 0, 0), Rotation()))
                          .shape('Part::Box', 'Box', Placement(Vector(5, 0, 0), Rotation()))
                          .assemble())

        resolved_objects = resolve_objects([transform_link])

        self.assertEqual(len(resolved_objects), 1)

        resolved_object = resolved_objects[0]
        resolved_shape = resolved_object['object']
        placement = resolved_object['placement']
        path = resolved_object['path']

        self.assertEqual(resolved_shape.TypeId, 'Part::Box')
        self.assertEqual(resolved_shape.Name, 'Box')
        self.assertPlacementEqual(placement, Placement(
            Vector(15, 0, 0), Rotation()))
        self.assertEqual(len(path), 2)
        self.assertEqual(path[0].TypeId, 'App::Link')
        self.assertEqual(path[0].LinkTransform, True)
        self.assertEqual(path[1].TypeId, 'App::Part')

    def test_resolve_objects_with_part_containing_link_to_shape(self):
        part = (Assembler()
                .part_containing(Placement(Vector(7, 0, 0), Rotation()))
                .link_to(Placement(Vector(1, 0, 0), Rotation()))
                .shape('Part::Box', 'Box', Placement(Vector(10, 0, 0), Rotation()))
                .assemble())

        resolved_objects = resolve_objects([part])

        self.assertEqual(len(resolved_objects), 1)

        resolved_object = resolved_objects[0]
        resolved_shape = resolved_object['object']
        placement = resolved_object['placement']
        path = resolved_object['path']

        self.assertEqual(resolved_shape.TypeId, 'Part::Box')
        self.assertEqual(resolved_shape.Name, 'Box')
        self.assertPlacementEqual(placement, Placement(
            Vector(8, 0, 0), Rotation()))
        self.assertEqual(len(path), 2)
        self.assertEqual(path[0].TypeId, 'App::Part')
        self.assertEqual(path[1].TypeId, 'App::Link')

    def test_resolve_objects_with_link_to_link_to_shape(self):
        link = (Assembler()
                .link_to(Placement(Vector(7, 0, 0), Rotation()))
                .link_to(Placement(Vector(1, 0, 0), Rotation()))
                .shape('Part::Box', 'Box', Placement(Vector(10, 0, 0), Rotation()))
                .assemble())

        resolved_objects = resolve_objects([link])

        self.assertEqual(len(resolved_objects), 1)

        resolved_object = resolved_objects[0]
        resolved_shape = resolved_object['object']
        placement = resolved_object['placement']
        path = resolved_object['path']

        self.assertEqual(resolved_shape.TypeId, 'Part::Box')
        self.assertEqual(resolved_shape.Name, 'Box')
        self.assertPlacementEqual(placement, Placement(
            Vector(7, 0, 0), Rotation()))
        self.assertEqual(len(path), 2)
        self.assertEqual(path[0].TypeId, 'App::Link')
        self.assertEqual(path[1].TypeId, 'App::Link')

    def test_resolve_objects_with_transform_link_to_link_to_shape(self):
        transform_link = (Assembler()
                          .transform_link_to(Placement(Vector(7, 0, 0), Rotation()))
                          .link_to(Placement(Vector(1, 0, 0), Rotation()))
                          .shape('Part::Box', 'Box', Placement(Vector(10, 0, 0), Rotation()))
                          .assemble())

        resolved_objects = resolve_objects([transform_link])

        self.assertEqual(len(resolved_objects), 1)

        resolved_object = resolved_objects[0]
        resolved_shape = resolved_object['object']
        placement = resolved_object['placement']
        path = resolved_object['path']

        self.assertEqual(resolved_shape.TypeId, 'Part::Box')
        self.assertEqual(resolved_shape.Name, 'Box')
        self.assertPlacementEqual(placement, Placement(
            Vector(8, 0, 0), Rotation()))
        self.assertEqual(len(path), 2)
        self.assertEqual(path[0].TypeId, 'App::Link')
        self.assertEqual(path[0].LinkTransform, True)
        self.assertEqual(path[1].TypeId, 'App::Link')

    def test_resolve_objects_with_part_containing_transform_link_to_shape(self):
        part = (Assembler()
                .part_containing(Placement(Vector(7, 0, 0), Rotation()))
                .transform_link_to(Placement(Vector(1, 0, 0), Rotation()))
                .shape('Part::Box', 'Box', Placement(Vector(10, 0, 0), Rotation()))
                .assemble())

        resolved_objects = resolve_objects([part])

        self.assertEqual(len(resolved_objects), 1)

        resolved_object = resolved_objects[0]
        resolved_shape = resolved_object['object']
        placement = resolved_object['placement']
        path = resolved_object['path']

        self.assertEqual(resolved_shape.TypeId, 'Part::Box')
        self.assertEqual(resolved_shape.Name, 'Box')
        self.assertPlacementEqual(placement, Placement(
            Vector(18, 0, 0), Rotation()))
        self.assertEqual(len(path), 2)
        self.assertEqual(path[0].TypeId, 'App::Part')
        self.assertEqual(path[1].TypeId, 'App::Link')
        self.assertEqual(path[1].LinkTransform, True)

    def test_resolve_objects_with_link_to_transform_link_to_shape(self):
        link = (Assembler()
                .link_to(Placement(Vector(7, 0, 0), Rotation()))
                .transform_link_to(Placement(Vector(1, 0, 0), Rotation()))
                .shape('Part::Box', 'Box', Placement(Vector(10, 0, 0), Rotation()))
                .assemble())

        resolved_objects = resolve_objects([link])

        self.assertEqual(len(resolved_objects), 1)

        resolved_object = resolved_objects[0]
        resolved_shape = resolved_object['object']
        placement = resolved_object['placement']
        path = resolved_object['path']

        self.assertEqual(resolved_shape.TypeId, 'Part::Box')
        self.assertEqual(resolved_shape.Name, 'Box')
        self.assertPlacementEqual(placement, Placement(
            Vector(17, 0, 0), Rotation()))
        self.assertEqual(len(path), 2)
        self.assertEqual(path[0].TypeId, 'App::Link')
        self.assertEqual(path[1].TypeId, 'App::Link')
        self.assertEqual(path[1].LinkTransform, True)

    def test_resolve_objects_with_transform_link_to_transform_link_to_shape(self):
        transform_link = (Assembler()
                          .transform_link_to(Placement(Vector(7, 0, 0), Rotation()))
                          .transform_link_to(Placement(Vector(1, 0, 0), Rotation()))
                          .shape('Part::Box', 'Box', Placement(Vector(10, 0, 0), Rotation()))
                          .assemble())

        resolved_objects = resolve_objects([transform_link])

        self.assertEqual(len(resolved_objects), 1)

        resolved_object = resolved_objects[0]
        resolved_shape = resolved_object['object']
        placement = resolved_object['placement']
        path = resolved_object['path']

        self.assertEqual(resolved_shape.TypeId, 'Part::Box')
        self.assertEqual(resolved_shape.Name, 'Box')
        self.assertPlacementEqual(placement, Placement(
            Vector(18, 0, 0), Rotation()))
        self.assertEqual(len(path), 2)
        self.assertEqual(path[0].TypeId, 'App::Link')
        self.assertEqual(path[0].LinkTransform, True)
        self.assertEqual(path[1].TypeId, 'App::Link')
        self.assertEqual(path[1].LinkTransform, True)

    def test_resolve_objects_with_rotated_part_containing_shapes(self):
        document = App.newDocument()
        cylinder = document.addObject('Part::Cylinder', 'Cylinder')
        cylinder.Height = 10
        cone = document.addObject('Part::Cone', 'Cone')
        cone.Radius2 = 0
        cone.Height = 4
        cone.Placement = Placement(
            Vector(0, 0, 10), Rotation())

        part = document.addObject('App::Part', 'Part')
        part.addObject(cylinder)
        part.addObject(cone)
        part.Placement = Placement(
            Vector(), Rotation(Vector(0, 1, 0), 90))

        resolved_objects = resolve_objects([part])

        self.assertEqual(len(resolved_objects), 2)

        resolved_cylinder = resolved_objects[0]
        cylinder = resolved_cylinder['object']
        cylinder_placement = resolved_cylinder['placement']
        cylinder_path = resolved_cylinder['path']
        self.assertEqual(cylinder.TypeId, 'Part::Cylinder')
        self.assertEqual(cylinder.Name, 'Cylinder')
        self.assertPlacementEqual(cylinder_placement, Placement(
            Vector(), Rotation(Vector(0, 1, 0), 90)))
        self.assertEqual(len(cylinder_path), 1)
        self.assertEqual(cylinder_path[0].TypeId, 'App::Part')

        resolved_cone = resolved_objects[1]
        cone = resolved_cone['object']
        cone_placement = resolved_cone['placement']
        cone_path = resolved_cone['path']
        self.assertEqual(cone.TypeId, 'Part::Cone')
        self.assertEqual(cone.Name, 'Cone')
        self.assertPlacementEqual(cone_placement, Placement(
            Vector(10, 0, 0), Rotation(Vector(0, 1, 0), 90)))
        self.assertEqual(len(cone_path), 1)
        self.assertEqual(cone_path[0].TypeId, 'App::Part')

    def test_resolve_objects_with_keep_unresolved_part_containing_shapes(self):
        document = App.newDocument()
        cylinder = document.addObject('Part::Cylinder', 'Cylinder')
        cylinder.Height = 10
        cone = document.addObject('Part::Cone', 'Cone')
        cone.Radius2 = 0
        cone.Height = 4
        cone.Placement = Placement(
            Vector(0, 0, 10), Rotation())

        part = document.addObject('App::Part', 'Part')
        part.addObject(cylinder)
        part.addObject(cone)
        part.Placement = Placement(
            Vector(), Rotation(Vector(0, 1, 0), 90))

        def keep_unresolved(obj: object, path: List[object]) -> bool:
            return obj.Name == 'Part'

        resolved_objects = resolve_objects([part], keep_unresolved)

        self.assertEqual(len(resolved_objects), 1)

        resolved_object = resolved_objects[0]
        part = resolved_object['object']
        placement = resolved_object['placement']
        path = resolved_object['path']

        self.assertEqual(part.TypeId, 'App::Part')
        self.assertEqual(part.Name, 'Part')
        self.assertPlacementEqual(placement, Placement(
            Vector(), Rotation(Vector(0, 1, 0), 90)))
        self.assertEqual(len(path), 0)

    def test_resolve_objects_with_keep_unresolved_link_to_shape(self):
        document = App.newDocument()
        shape = document.addObject('Part::Cylinder', 'Cylinder')
        shape.Placement = Placement(
            Vector(5, 0, 0), Rotation())

        link = document.addObject('App::Link', 'CylinderLink')
        link.setLink(shape)
        link.Placement = Placement(
            Vector(10, 0, 0), Rotation())

        def keep_unresolved(obj: object, path: List[object]) -> bool:
            return obj.Name == 'CylinderLink'

        resolved_objects = resolve_objects([link], keep_unresolved)

        self.assertEqual(len(resolved_objects), 1)

        resolved_object = resolved_objects[0]
        resolved_shape = resolved_object['object']
        placement = resolved_object['placement']
        path = resolved_object['path']

        self.assertEqual(resolved_shape.TypeId, 'App::Link')
        self.assertEqual(resolved_shape.Name, 'CylinderLink')
        self.assertPlacementEqual(placement, Placement(
            Vector(10, 0, 0), Rotation()))
        self.assertEqual(len(path), 0)

    def test_resolve_objects_with_keep_unresolved_transform_link_to_shape(self):
        document = App.newDocument()
        shape = document.addObject('Part::Cylinder', 'Cylinder')
        shape.Placement = Placement(
            Vector(5, 0, 0), Rotation())

        link = document.addObject('App::Link', 'CylinderLink')
        link.setLink(shape)
        link.Placement = Placement(
            Vector(10, 0, 0), Rotation())
        link.LinkTransform = True

        def keep_unresolved(obj: object, path: List[object]) -> bool:
            return obj.Name == 'CylinderLink'

        resolved_objects = resolve_objects([link], keep_unresolved)

        self.assertEqual(len(resolved_objects), 1)

        resolved_object = resolved_objects[0]
        resolved_shape = resolved_object['object']
        placement = resolved_object['placement']
        path = resolved_object['path']

        self.assertEqual(resolved_shape.TypeId, 'App::Link')
        self.assertEqual(resolved_shape.LinkTransform, True)
        self.assertEqual(resolved_shape.Name, 'CylinderLink')
        self.assertPlacementEqual(placement, Placement(
            Vector(15, 0, 0), Rotation()))
        self.assertEqual(len(path), 0)

    def assertPlacementEqual(self, a, b):
        self.assertAlmostEqual(a.Base.x, b.Base.x, places=3)
        self.assertAlmostEqual(a.Base.y, b.Base.y, places=3)
        self.assertAlmostEqual(a.Base.z, b.Base.z, places=3)

        self.assertEqual(a.Rotation.Angle, b.Rotation.Angle)
        self.assertEqual(a.Rotation.Axis, b.Rotation.Axis)


if __name__ == '__main__':
    unittest.main()
