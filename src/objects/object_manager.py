from collections import defaultdict
import bpy

class ObjectManager:
    
    def copy_objects(self, from_col, to_col, dupe_lut):
        # copy all objects from one collection to another
        for obj in from_col.objects:
            dupe = obj.copy()
            dupe.data = dupe.data.copy()
            to_col.objects.link(dupe)
            dupe_lut[obj] = dupe

    def copy(self, parent, collection):
        # recursively copy a collection and all its children
        dupe_lut = defaultdict(lambda : None)
        def _copy(parent, collection):
            cc = bpy.data.collections.new(collection.name)
            self.copy_objects(collection, cc, dupe_lut)

            for c in collection.children:
                _copy(cc, c)

            parent.children.link(cc)
        
        _copy(parent, collection)
        # print(dupe_lut)
        for obj, dupe in tuple(dupe_lut.items()):
            parent = dupe_lut[obj.parent]
            if parent:
                dupe.parent = parent
                
                
    def CheckSelectStatus(self, p):
        for c in p.children:
            print(c.name)
            c['hideSelectWasTrue'] = False
            if bpy.data.objects[c.name].hide_select == True:
                bpy.data.objects[c.name].hide_select = False
                c['hideSelectWasTrue'] = True
            c.select = True
            self.CheckSelectStatus(c)

    def RestoreSelectStatus(self, p):
        for c in p.children:
            if c['hideSelectWasTrue'] == True:
                bpy.data.objects[c.name].hide_select = True
            self.RestoreSelectStatus(c)