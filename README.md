# FreeCAD: Export to OBJ
Python package to export FreeCAD objects to the [Wavefront (.obj)](https://en.wikipedia.org/wiki/Wavefront_.obj_file) file format.

## Why this package?
This package satisfies some unique requirements for exporting to OBJ that FreeCAD's built-in functions do not currently satisfy:

* Return a string or the file's contents; instead of writing to a file immediately.
* Use an object's `Label` for the object's name in the `.obj` file.
* Ungroup the following standard container objects:
  * [Group](https://wiki.freecadweb.org/Std_Group)
  * [Part](https://wiki.freecadweb.org/Std_Part)

## Usage

```python
import freecad_to_obj
obj_file_contents = freecad_to_obj.export(objects)
```

## Contributing
See [Contributing Guidelines](./CONTRIBUTING.md).

## Limitations
For simplicity, this package does not care about thes generation of material (`.mtl`) files.

## Supported FreeCAD Versions
Currently tested with FreeCAD `19.1`.
