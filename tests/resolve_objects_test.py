import unittest

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
            Vector(10, 0, 0), Rotation(Vector(0, 0, 1), 0)))

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
            Vector(10, 0, 0), Rotation(Vector(0, 0, 1), 0)))

    def assertPlacementEqual(self, a, b):
        self.assertAlmostEqual(a.Base.x, b.Base.x, places=3)
        self.assertAlmostEqual(a.Base.y, b.Base.y, places=3)
        self.assertAlmostEqual(a.Base.z, b.Base.z, places=3)

        self.assertEqual(a.Rotation.Angle, b.Rotation.Angle)
        self.assertEqual(a.Rotation.Axis, b.Rotation.Axis)


if __name__ == '__main__':
    unittest.main()
