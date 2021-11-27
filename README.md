# freecad-to-obj

[![PyPI version](https://badge.fury.io/py/freecad-to-obj.svg)](https://badge.fury.io/py/freecad-to-obj)

Python package to export FreeCAD objects to the [Wavefront (.obj)](https://en.wikipedia.org/wiki/Wavefront_.obj_file) file format.

## Why this package?
This package satisfies some unique requirements for exporting to OBJ that FreeCAD's built-in functions do not currently satisfy:

* Return a string or the file's contents; instead of writing to a file immediately.
* Use an object's `Label` for the object's name in the `.obj` file.
* Ungroup the following standard container objects:
  * [Group](https://wiki.freecadweb.org/Std_Group)
  * [Part](https://wiki.freecadweb.org/Std_Part)
* Control export granularity keeping container objects grouped, and links unresolved.
* Control which objects are exported (e.g. don't export invisible objects).
* Export wires (the black outline or line segments surrounding parts)

## Usage

```python
import freecad_to_obj
obj_file_contents = freecad_to_obj.export(objects)
```

## Export Format
Object names in Wavefront .obj are preceded by an "o [ObjectName]" ([source](https://en.wikipedia.org/wiki/Wavefront_.obj_file#Reference_materials)).

This library uses the object's `Label` for the object name by default, but you can change this behavior via the `object_name_getter` keyword argument (see [API](#api)).

    o [ObjectName]
    v [x1] [y1] [y2]
    v ...
    vn [x1] [y1] [y2]
    vn ...
    f v1//vn1 v2//vn2 v3//vn3 ...

After the object name are:

* **v**ertices preceded by `v`
* **v**ertex normals preceded by `vn`
* and **f**aces preceded by `f`
  * faces reference the vertices and vertex normals by number (starting from **1** instead of 0)

Combined these make up the geometry for the object.

Wires for objects are exported as separate objects in the form:

    [ObjectName]WireN
    v [x1] [y1] [y2]
    v ...
    l v1 v2 v3 ...

Where `N` is a zero-indexed incrementing counter.

For example:

    o ExampleObjectWire0
    ...
    o ExampleObjectWire1
    ...
    o ExampleObjectWire2

After the object name are:

* **v**ertices preceded by `v`
* and **l**ine segments preceded by `l`
  * line segments reference the vertices by number (starting from **1** instead of 0)

## API

### export(objects)

Exports a list of FreeCAD objects to Wavefront (.obj).

#### Arguments

|Name|Type|Required|Description|
|----|----|--------|-----------|
|`objects`|`List[object]`|`true`|List of FreeCAD objects to export|

#### Keyword Arguments

|Name|Type|Default|Description|
|----|----|--------|-----------|
|`object_name_getter`|`Callable[[object, List[object]], str]`|`lambda obj, path: obj.Label`|Defaults to the `Label`.|Function to return the name of the object used in export.|
|` keep_unresolved`|`Callable[[object, List[object]], bool]`|`None`|Function to return whether to keep an object "unresolved" or a group such as `App::Link` or `App::Part`.|
|`do_not_export`|`Callable[[object, List[object]], bool]`|`lambda obj, path: not obj.Visibility`|Function to return whether to export an object or not. By default, all invisible objects are *not* exported.|

**Returns:** (`string`) Wavefront .obj file contents.

## Contributing
See [Contributing Guidelines](./CONTRIBUTING.md).

## Changelog
See [Changelog](./CHANGELOG.md).

## Limitations
For simplicity, this package does not care about thes generation of material (`.mtl`) files.

## Supported FreeCAD Versions
Currently tested with FreeCAD `19.1`.
