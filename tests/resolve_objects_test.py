import unittest

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

        resolved_shape, placement = resolved_objects[0]
        self.assertEqual(resolved_shape.TypeId, 'Part::Box')
        self.assertEqual(resolved_shape.Name, 'Box')
        self.assertPlacementEqual(placement, Placement(
            Vector(10, 0, 0), Rotation()))

    def test_resolve_objects_with_part_containing_shape(self):
        part = (Assembler()
                .part_containing(Placement(Vector(5, 0, 0), Rotation()))
                .shape('Part::Box', 'Box', Placement(Vector(5, 0, 0), Rotation()))
                .assemble())

        resolved_objects = resolve_objects([part])

        self.assertEqual(len(resolved_objects), 1)

        resolved_shape, placement = resolved_objects[0]
        self.assertEqual(resolved_shape.TypeId, 'Part::Box')
        self.assertEqual(resolved_shape.Name, 'Box')
        self.assertPlacementEqual(placement, Placement(
            Vector(10, 0, 0), Rotation()))

    def test_resolve_objects_with_link_to_shape(self):
        link = (Assembler()
                .link_to(Placement(Vector(10, 0, 0), Rotation()))
                .shape('Part::Box', 'Box', Placement(Vector(5, 0, 0), Rotation()))
                .assemble())

        resolved_objects = resolve_objects([link])

        self.assertEqual(len(resolved_objects), 1)

        resolved_shape, placement = resolved_objects[0]
        self.assertEqual(resolved_shape.TypeId, 'Part::Box')
        self.assertEqual(resolved_shape.Name, 'Box')
        self.assertPlacementEqual(placement, Placement(
            Vector(10, 0, 0), Rotation()))

    def test_resolve_objects_with_transform_link_to_shape(self):
        transform_link = (Assembler()
                          .transform_link_to(Placement(Vector(10, 0, 0), Rotation()))
                          .shape('Part::Box', 'Box', Placement(Vector(5, 0, 0), Rotation()))
                          .assemble())

        resolved_objects = resolve_objects([transform_link])

        self.assertEqual(len(resolved_objects), 1)

        resolved_shape, placement = resolved_objects[0]
        self.assertEqual(resolved_shape.TypeId, 'Part::Box')
        self.assertEqual(resolved_shape.Name, 'Box')
        self.assertPlacementEqual(placement, Placement(
            Vector(15, 0, 0), Rotation()))

    def test_resolve_objects_with_part_containing_part_containing_shape(self):
        part = (Assembler()
                .part_containing(Placement(Vector(5, 0, 0), Rotation()))
                .part_containing(Placement(Vector(5, 0, 0), Rotation()))
                .shape('Part::Box', 'Box', Placement(Vector(5, 0, 0), Rotation()))
                .assemble())

        resolved_objects = resolve_objects([part])

        self.assertEqual(len(resolved_objects), 1)

        resolved_shape, placement = resolved_objects[0]
        self.assertEqual(resolved_shape.TypeId, 'Part::Box')
        self.assertEqual(resolved_shape.Name, 'Box')
        self.assertPlacementEqual(placement, Placement(
            Vector(15, 0, 0), Rotation()))

    def test_resolve_objects_with_link_to_part_containing_shape(self):
        link = (Assembler()
                .link_to(Placement(Vector(10, 0, 0), Rotation()))
                .part_containing(Placement(Vector(100, 0, 0), Rotation()))
                .shape('Part::Box', 'Box', Placement(Vector(3, 0, 0), Rotation()))
                .assemble())

        resolved_objects = resolve_objects([link])

        self.assertEqual(len(resolved_objects), 1)

        resolved_shape, placement = resolved_objects[0]
        self.assertEqual(resolved_shape.TypeId, 'Part::Box')
        self.assertEqual(resolved_shape.Name, 'Box')
        self.assertPlacementEqual(placement, Placement(
            Vector(13, 0, 0), Rotation()))

    def test_resolve_objects_with_transform_link_to_part_containing_shape(self):
        transform_link = (Assembler()
                          .transform_link_to(Placement(Vector(5, 0, 0), Rotation()))
                          .part_containing(Placement(Vector(5, 0, 0), Rotation()))
                          .shape('Part::Box', 'Box', Placement(Vector(5, 0, 0), Rotation()))
                          .assemble())

        resolved_objects = resolve_objects([transform_link])

        self.assertEqual(len(resolved_objects), 1)

        resolved_shape, placement = resolved_objects[0]
        self.assertEqual(resolved_shape.TypeId, 'Part::Box')
        self.assertEqual(resolved_shape.Name, 'Box')
        self.assertPlacementEqual(placement, Placement(
            Vector(15, 0, 0), Rotation()))

    def test_resolve_objects_with_part_containing_link_to_shape(self):
        part = (Assembler()
                .part_containing(Placement(Vector(7, 0, 0), Rotation()))
                .link_to(Placement(Vector(1, 0, 0), Rotation()))
                .shape('Part::Box', 'Box', Placement(Vector(10, 0, 0), Rotation()))
                .assemble())

        resolved_objects = resolve_objects([part])

        self.assertEqual(len(resolved_objects), 1)

        resolved_shape, placement = resolved_objects[0]
        self.assertEqual(resolved_shape.TypeId, 'Part::Box')
        self.assertEqual(resolved_shape.Name, 'Box')
        self.assertPlacementEqual(placement, Placement(
            Vector(8, 0, 0), Rotation()))

    def test_resolve_objects_with_link_to_link_to_shape(self):
        link = (Assembler()
                .link_to(Placement(Vector(7, 0, 0), Rotation()))
                .link_to(Placement(Vector(1, 0, 0), Rotation()))
                .shape('Part::Box', 'Box', Placement(Vector(10, 0, 0), Rotation()))
                .assemble())

        resolved_objects = resolve_objects([link])

        self.assertEqual(len(resolved_objects), 1)

        resolved_shape, placement = resolved_objects[0]
        self.assertEqual(resolved_shape.TypeId, 'Part::Box')
        self.assertEqual(resolved_shape.Name, 'Box')
        self.assertPlacementEqual(placement, Placement(
            Vector(7, 0, 0), Rotation()))

    def test_resolve_objects_with_transform_link_to_link_to_shape(self):
        transform_link = (Assembler()
                          .transform_link_to(Placement(Vector(7, 0, 0), Rotation()))
                          .link_to(Placement(Vector(1, 0, 0), Rotation()))
                          .shape('Part::Box', 'Box', Placement(Vector(10, 0, 0), Rotation()))
                          .assemble())

        resolved_objects = resolve_objects([transform_link])

        self.assertEqual(len(resolved_objects), 1)

        resolved_shape, placement = resolved_objects[0]
        self.assertEqual(resolved_shape.TypeId, 'Part::Box')
        self.assertEqual(resolved_shape.Name, 'Box')
        self.assertPlacementEqual(placement, Placement(
            Vector(8, 0, 0), Rotation()))

    def test_resolve_objects_with_part_containing_transform_link_to_shape(self):
        part = (Assembler()
                .part_containing(Placement(Vector(7, 0, 0), Rotation()))
                .transform_link_to(Placement(Vector(1, 0, 0), Rotation()))
                .shape('Part::Box', 'Box', Placement(Vector(10, 0, 0), Rotation()))
                .assemble())

        resolved_objects = resolve_objects([part])

        self.assertEqual(len(resolved_objects), 1)

        resolved_shape, placement = resolved_objects[0]
        self.assertEqual(resolved_shape.TypeId, 'Part::Box')
        self.assertEqual(resolved_shape.Name, 'Box')
        self.assertPlacementEqual(placement, Placement(
            Vector(18, 0, 0), Rotation()))

    def test_resolve_objects_with_link_to_transform_link_to_shape(self):
        link = (Assembler()
                .link_to(Placement(Vector(7, 0, 0), Rotation()))
                .transform_link_to(Placement(Vector(1, 0, 0), Rotation()))
                .shape('Part::Box', 'Box', Placement(Vector(10, 0, 0), Rotation()))
                .assemble())

        resolved_objects = resolve_objects([link])

        self.assertEqual(len(resolved_objects), 1)

        resolved_shape, placement = resolved_objects[0]
        self.assertEqual(resolved_shape.TypeId, 'Part::Box')
        self.assertEqual(resolved_shape.Name, 'Box')
        self.assertPlacementEqual(placement, Placement(
            Vector(17, 0, 0), Rotation()))

    def test_resolve_objects_with_transform_link_to_transform_link_to_shape(self):
        transform_link = (Assembler()
                          .transform_link_to(Placement(Vector(7, 0, 0), Rotation()))
                          .transform_link_to(Placement(Vector(1, 0, 0), Rotation()))
                          .shape('Part::Box', 'Box', Placement(Vector(10, 0, 0), Rotation()))
                          .assemble())

        resolved_objects = resolve_objects([transform_link])

        self.assertEqual(len(resolved_objects), 1)

        resolved_shape, placement = resolved_objects[0]
        self.assertEqual(resolved_shape.TypeId, 'Part::Box')
        self.assertEqual(resolved_shape.Name, 'Box')
        self.assertPlacementEqual(placement, Placement(
            Vector(18, 0, 0), Rotation()))

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

        resolved_cylinder, cylinder_placement = resolved_objects[0]
        self.assertEqual(resolved_cylinder.TypeId, 'Part::Cylinder')
        self.assertEqual(resolved_cylinder.Name, 'Cylinder')
        self.assertPlacementEqual(cylinder_placement, Placement(
            Vector(), Rotation(Vector(0, 1, 0), 90)))

        resolved_cone, cone_placement = resolved_objects[1]
        self.assertEqual(resolved_cone.TypeId, 'Part::Cone')
        self.assertEqual(resolved_cone.Name, 'Cone')
        self.assertPlacementEqual(cone_placement, Placement(
            Vector(10, 0, 0), Rotation(Vector(0, 1, 0), 90)))

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

        def keep_unresolved(obj):
            return obj.Name == 'Part'

        resolved_objects = resolve_objects([part], keep_unresolved)

        self.assertEqual(len(resolved_objects), 1)

        resolved_cylinder, cylinder_placement = resolved_objects[0]
        self.assertEqual(resolved_cylinder.TypeId, 'App::Part')
        self.assertEqual(resolved_cylinder.Name, 'Part')
        self.assertPlacementEqual(cylinder_placement, Placement(
            Vector(), Rotation(Vector(0, 1, 0), 90)))

    def test_resolve_objects_with_keep_unresolved_link_to_shape(self):
        document = App.newDocument()
        shape = document.addObject('Part::Cylinder', 'Cylinder')
        shape.Placement = Placement(
            Vector(5, 0, 0), Rotation())

        link = document.addObject('App::Link', 'CylinderLink')
        link.setLink(shape)
        link.Placement = Placement(
            Vector(10, 0, 0), Rotation())

        def keep_unresolved(obj):
            return obj.Name == 'CylinderLink'

        resolved_objects = resolve_objects([link], keep_unresolved)

        self.assertEqual(len(resolved_objects), 1)

        resolved_shape, placement = resolved_objects[0]
        self.assertEqual(resolved_shape.TypeId, 'App::Link')
        self.assertEqual(resolved_shape.Name, 'CylinderLink')
        self.assertPlacementEqual(placement, Placement(
            Vector(10, 0, 0), Rotation()))

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

        def keep_unresolved(obj):
            return obj.Name == 'CylinderLink'

        resolved_objects = resolve_objects([link], keep_unresolved)

        self.assertEqual(len(resolved_objects), 1)

        resolved_shape, placement = resolved_objects[0]
        self.assertEqual(resolved_shape.TypeId, 'App::Link')
        self.assertEqual(resolved_shape.Name, 'CylinderLink')
        self.assertPlacementEqual(placement, Placement(
            Vector(15, 0, 0), Rotation()))

    def assertPlacementEqual(self, a, b):
        self.assertAlmostEqual(a.Base.x, b.Base.x, places=3)
        self.assertAlmostEqual(a.Base.y, b.Base.y, places=3)
        self.assertAlmostEqual(a.Base.z, b.Base.z, places=3)

        self.assertEqual(a.Rotation.Angle, b.Rotation.Angle)
        self.assertEqual(a.Rotation.Axis, b.Rotation.Axis)


if __name__ == '__main__':
    unittest.main()
