# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2021-11-27
### Added
- Ability to export FreeCAD objects to the  Wavefront (.obj) file format.
- Control the name of the object used in the export via `object_name_getter`
- Control export granularity via `keep_unresolved`
- Control which objects are exported via `do_not_export`. By default, all invisible objects are *not* exported.

[Unreleased]: https://github.com/gbroques/freecad-to-obj/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/gbroques/freecad-to-obj/releases/tag/v0.1.0
