from itertools import tee

import FreeCAD as App

__all__ = ['Assembler']


class Assembler:

    def __init__(self):
        self.document = App.newDocument()
        self.objects = []

    def part_containing(self, placement):
        part = self.document.addObject('App::Part', 'Part')
        part.Placement = placement
        self.objects.append(part)
        return self

    def link_to(self, placement):
        link = self.document.addObject('App::Link', 'Link')
        link.Placement = placement
        self.objects.append(link)
        return self

    def transform_link_to(self, placement):
        link = self.document.addObject('App::Link', 'Link')
        link.Placement = placement
        link.LinkTransform = True
        self.objects.append(link)
        return self

    def shape(self, object_type, name, placement):
        shape = self.document.addObject(object_type, name)
        shape.Placement = placement
        self.objects.append(shape)
        return self

    def assemble(self):
        for first, second in pairwise(self.objects):
            if second is not None:
                if first.TypeId == 'App::Part':
                    first.addObject(second)
                elif first.TypeId == 'App::Link':
                    first.setLink(second)
        self.document.recompute()
        return self.objects[0] if len(self.objects) > 0 else None


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)
