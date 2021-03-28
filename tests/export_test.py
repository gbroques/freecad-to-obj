import os
import unittest

import FreeCAD as App
import freecad_to_obj


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


if __name__ == '__main__':
    unittest.main()
