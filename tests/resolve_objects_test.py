import os
import unittest

import FreeCAD as App
from FreeCAD import Placement, Rotation, Vector
from freecad_to_obj.resolve_objects import resolve_objects


class ResolveObjectsTest(unittest.TestCase):

    def test_resolve_objects_with_primitive(self):
        document = App.newDocument()
        primitive = document.addObject('Part::Box', 'Box')
        document.recompute()

        resolved_objects = resolve_objects([primitive])

        self.assertEqual(len(resolved_objects), 1)

        resolved_primitive, placement = resolved_objects[0]
        self.assertEqual(resolved_primitive.TypeId, 'Part::Box')
        self.assertEqual(resolved_primitive.Name, 'Box')
        self.assertPlacementEqual(placement, Placement())

    def test_resolve_objects_with_translated_primitive(self):
        document = App.newDocument()
        translated_primitive = document.addObject('Part::Box', 'Box')
        translated_primitive.Placement = Placement(
            Vector(10, 0, 0), Rotation(Vector(0, 0, 1), 0))
        document.recompute()

        resolved_objects = resolve_objects([translated_primitive])

        self.assertEqual(len(resolved_objects), 1)

        resolved_primitive, placement = resolved_objects[0]
        self.assertEqual(resolved_primitive.TypeId, 'Part::Box')
        self.assertEqual(resolved_primitive.Name, 'Box')
        self.assertPlacementEqual(placement, Placement(
            Vector(10, 0, 0), Rotation(Vector(0, 0, 1), 0)))

    def test_resolve_objects_with_part_containing_primitive(self):
        document = App.newDocument()
        primitive = document.addObject('Part::Box', 'Box')
        part = document.addObject('App::Part', 'Part')
        part.addObject(primitive)
        document.recompute()

        resolved_objects = resolve_objects([part])

        self.assertEqual(len(resolved_objects), 1)

        resolved_primitive, placement = resolved_objects[0]
        self.assertEqual(resolved_primitive.TypeId, 'Part::Box')
        self.assertEqual(resolved_primitive.Name, 'Box')
        self.assertPlacementEqual(placement, Placement())

    def test_resolve_objects_with_part_containing_translated_primitive(self):
        document = App.newDocument()
        translated_primitive = document.addObject('Part::Box', 'Box')
        translated_primitive.Placement = Placement(
            Vector(10, 0, 0), Rotation(Vector(0, 0, 1), 0))
        part = document.addObject('App::Part', 'Part')
        part.addObject(translated_primitive)
        document.recompute()

        resolved_objects = resolve_objects([part])

        self.assertEqual(len(resolved_objects), 1)

        resolved_primitive, placement = resolved_objects[0]
        self.assertEqual(resolved_primitive.TypeId, 'Part::Box')
        self.assertEqual(resolved_primitive.Name, 'Box')
        self.assertPlacementEqual(placement, Placement(
            Vector(10, 0, 0), Rotation(Vector(0, 0, 1), 0)))

    def test_resolve_objects_with_translated_part_containing_primitive(self):
        document = App.newDocument()
        primitive = document.addObject('Part::Box', 'Box')
        translated_part = document.addObject('App::Part', 'Part')
        translated_part.Placement = Placement(
            Vector(10, 0, 0), Rotation(Vector(0, 0, 1), 0))
        translated_part.addObject(primitive)
        document.recompute()

        resolved_objects = resolve_objects([translated_part])

        self.assertEqual(len(resolved_objects), 1)

        resolved_primitive, placement = resolved_objects[0]
        self.assertEqual(resolved_primitive.TypeId, 'Part::Box')
        self.assertEqual(resolved_primitive.Name, 'Box')
        self.assertPlacementEqual(placement, Placement(
            Vector(10, 0, 0), Rotation(Vector(0, 0, 1), 0)))

    def test_resolve_objects_with_translated_part_containing_translated_primitive(self):
        document = App.newDocument()
        translated_primitive = document.addObject('Part::Box', 'Box')
        translated_primitive.Placement = Placement(
            Vector(5, 0, 0), Rotation(Vector(0, 0, 1), 0))
        translated_part = document.addObject('App::Part', 'Part')
        translated_part.Placement = Placement(
            Vector(5, 0, 0), Rotation(Vector(0, 0, 1), 0))
        translated_part.addObject(translated_primitive)
        document.recompute()

        resolved_objects = resolve_objects([translated_part])

        self.assertEqual(len(resolved_objects), 1)

        resolved_primitive, placement = resolved_objects[0]
        self.assertEqual(resolved_primitive.TypeId, 'Part::Box')
        self.assertEqual(resolved_primitive.Name, 'Box')
        self.assertPlacementEqual(placement, Placement(
            Vector(10, 0, 0), Rotation(Vector(0, 0, 1), 0)))

    def assertPlacementEqual(self, a, b):
        self.assertAlmostEqual(a.Base.x, b.Base.x, places=3)
        self.assertAlmostEqual(a.Base.y, b.Base.y, places=3)
        self.assertAlmostEqual(a.Base.z, b.Base.z, places=3)

        self.assertEqual(a.Rotation.Angle, b.Rotation.Angle)
        self.assertEqual(a.Rotation.Axis, b.Rotation.Axis)


if __name__ == '__main__':
    unittest.main()
