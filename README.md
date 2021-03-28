# FreeCAD: Export to OBJ
Python package to export FreeCAD objects to the [Wavefront (.obj)](https://en.wikipedia.org/wiki/Wavefront_.obj_file) file format.

## Why this package?
FreeCAD has two built-in functions for exporting to OBJ:

1. From the `Mesh` module.
2. From the `Arch` module.

Both functions have the following limitations:

1. Use an object's `Name` instead of `Label`
2. and write to a file immediately instead of providing a string or the file's contents.

Additionally, the `Arch` module's export to OBJ function lacks the ability to export [`App::Part`](https://wiki.freecadweb.org/App_Part)s.

## Usage

```python
import freecad_to_obj
obj_file_contents = freecad_to_obj.export(objects)
```

## Contributing
See [Contributing Guidelines](./CONTRIBUTING.md).

## Supported FreeCAD Versions
Currently tested with FreeCAD `19.1`.
