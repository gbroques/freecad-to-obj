import os
import unittest

import FreeCAD as App
from FreeCAD import Placement
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
        self.assertPlacementEqual(placement, primitive.Placement)

    def assertPlacementEqual(self, a, b):
        self.assertAlmostEqual(a.Base.x, b.Base.x, places=3)
        self.assertAlmostEqual(a.Base.y, b.Base.y, places=3)
        self.assertAlmostEqual(a.Base.z, b.Base.z, places=3)

        self.assertEqual(a.Rotation.Angle, b.Rotation.Angle)
        self.assertEqual(a.Rotation.Axis, b.Rotation.Axis)


if __name__ == '__main__':
    unittest.main()
