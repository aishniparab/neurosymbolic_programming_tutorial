"""
Need to fix:
* return list of objects as an object set with the correct indices
* refactor objectset
"""
class ClevrObject: # data type
    def __init__(self):
        #, image_filename, object_idx, pixel_coords, three_d_coords, rotation, size, color, shape,
        #         material):
        self.image_idx = None #image_filename
        self.object_idx = None #object_idx  # in the scene
        self.pixel_coords = None #pixel_coords
        self.three_d_coords = None #three_d_coords
        self.rotation = None #rotation
        self.size = None #size
        self.color = None #color
        self.shape = None #shape
        self.material = None #material

    def set_attr(self, attr_name, attr):
        if attr_name.lower() == "size":
            self.size = Size(attr)
        elif attr_name.lower() == "color":
            self.color = Color(attr)
        elif attr_name.lower() == "shape":
            self.shape = Shape(attr)
        elif attr_name.lower() == "material":
            self.material = Material(attr)
        elif attr_name == "image_idx":
            self.image_idx = attr
        elif attr_name == "object_idx":
            self.object_idx = attr
        elif attr_name == "pixel_coords":
            self.pixel_coords = attr
        elif attr_name == "three_d_coords":
            self.three_d_coords = attr
        elif attr_name == "rotation":
            self.rotation == attr
        else:
            return "Invalid attribute"

    @staticmethod
    def get_attr(input_string):
        """
        :param x: string: an object attribute such as "small" or "sphere"
        :return: string: name of the attribute category it belongs to such as "size" or "shape"
        """
        # space of object attribute defined in the DSL
        attribute_space = {
            'size': ["small", "large"],
            'color': ["gray", "red", "blue", "green", "brown", "purple", "cyan", "yellow"],
            'shape': ["cube", "sphere", "cylinder"],
            'material': ["rubber", "metal"]
        }
        return [k for k, v in attribute_space.items() if input_string in v][0]

"""
class ClevrObjectSet: # data type
    def __init__(self, image_filename, scene_objects):
        self.objects = [
            ClevrObject(image_filename, obj_idx, obj['pixel_coords'], obj['3d_coords'], obj['rotation'], obj['size'],
                        obj['color'], obj['shape'], obj['material']) for obj_idx, obj in enumerate(scene_objects)]
        self.size = len(scene_objects)
"""

class ClevrScene:
    # input is a single scene
    def __init__(self, scene_graph):  # output is an object set
        self.num_objects = len(scene_graph['objects'])
        self.relationships = scene_graph[
            'relationships']  # [obj1[list of objs to the right of obj1], obj2[], ..., objN[]]
        self.directions = scene_graph['directions']
        self.split = scene_graph['split']  # train, val, test
        self.image_idx = scene_graph['image_index']
        self.image_filename = scene_graph['image_filename']
        self.ObjectSet = ClevrObjectSet(self.image_filename, scene_graph['objects'])

class Boolean: # data type
    def __init__(self, term):
        self.boolean_space = {
            'true': 'yes',
            True: 'yes',
            'True': 'yes',
            '1': 'yes',
            False: 'no',
            'false': 'no',
            'False': 'no',
            '0': 'no'
        }
        if term in self.boolean_space:
            self.value = self.value_space[term]
        else:
            return "Boolean undefined in vocabulary"
class Integer: # data type
    def __init__(self, term):
        self.integer_space = {
            '0': 0,
            'zero': 0,
            '1': 1,
            'one': 1,
            '2': 2,
            'two': 2,
            '3': 3,
            'three': 3,
            '4': 4,
            'four': 4,
            '5': 5,
            'five': 5,
            '6': 6,
            'six': 6,
            '7': 7,
            'seven': 7,
            '8': 8,
            'eight': 8,
            '9': 9,
            'nine': 9,
            '10': 10,
            'ten': 10
        }
        if term in self.integer_space:
            self.value = self.integer_space[term]
        else:
            return "Integer undefined in vocabulary"

class Color: #value type
    def __init__(self, term):
        self.color_space = {'blue', 'red', 'green', 'cyan', 'gray', 'brown', 'purple', 'yellow'}
        if term in self.color_space:
            self.value = term
        else:
            return "Color undefined in vocabulary"

class Size: #value type
    def __init__(self, term):
        self.size_space = {
            'large': 'large', 'big': 'large',
            'small': 'small', 'tiny': 'small'}
        if term in self.size_space:
            self.value = self.size_space[term]
        else:
            return "Size undefined in vocabulary"

class Material: #value type
    def __init__(self, term):
        self.material_space = {
            'metal': 'metal', 'shiny': 'metal', 'metallic': 'metal',
            'rubber': 'rubber', 'matte': 'rubber'}
        if term in self.material_space:
            self.value = self.material_space[term]
        else:
            "Material undefined in vocabulary"

class Shape: #value type
    def __init__(self, term):
        self.shape_space = {
            'cube': 'cube', 'block': 'cube',
            'sphere': 'sphere', 'ball': 'sphere',
            'cylinder': 'cylinder'
        }
        if term in self.shape_space:
            self.value = self.shape_space[term]
        else:
            "Shape undefined in vocabulary"
class Relation: #value type
    def __init__(self, term):
        self.relation_space = {
            'front': 'front', 'in front of': 'front',
            'behind': 'behind',
            'right': 'right', 'right of': 'right', 'to the right of': 'right', 'on the right side of': 'right',
            'left': 'left', 'left of': 'left', 'to the left of': 'left', 'on the left side of': 'left',
            'above': 'above',
            'below': 'below'
        }
        if term in self.relation_space:
            self.value = self.relation_space[term]
        else:
            return "Relation undefined in vocabulary"
class ClevrDSL:
    def __init__(self, image_idx, scene_graph):
        self.this_scene = ClevrScene(scene_graph)
        self.yes = Boolean(True).value
        self.no = Boolean(False).value

    def scene(self):
        """
        :return: set of all objects in the scene
        """
        return self.this_scene.ObjectSet

    @staticmethod
    def unique(obj_set):
        """
        :param obj_set: ClevrObjectSet() object
        :return: if input is a singleton set return it as an Object otherwise raise exception
        """
        if len(obj_set) == 1:
            return ClevrObject(obj_set[0])
        else:
            raise Exception("Question is ill-posed")

    def relate(self, obj, relation):
        """
        :param obj: ClevrObject()
        :param relation: string
        :return: Return all objects in the scene that have the specified spatial relation
        to the input object.
        """
        # get a list of object indices that are to the <relation> of the object
        related_objects_idx = self.this_scene.relationships[relation][obj.object_idx]
        # return a list of ClevrObject()
        return [self.this_scene.ObjectSet[idx] for idx in related_objects_idx]

    @staticmethod
    def count(obj_set):
        """
        :param obj_set: ClevrObjectSet()
        :return: integer: size of the input set
        """
        return obj_set.size

    def exist(self, obj_set):
        """
        :param obj_set: ClevrObjectSet()
        :return: boolean: Yes if input is non-empty, No otherwise
        """
        if obj_set.size > 0:
            return self.yes
        else:
            return self.no

    @staticmethod
    def filter_size(obj_set, size):
        """
        :param obj_set: ClevrObjectSet()
        :param size: string
        :return: select objects in objectset if its size matches input
        """
        return [obj for obj in obj_set.objects if obj.size == size]

    @staticmethod
    def filter_color(obj_set, color):
        """
        :param obj_set: ClevrObjectSet()
        :param color: string
        :return: select objects in objectset if its color matches input
        """
        return [obj for obj in obj_set.objects if obj.color == color]

    @staticmethod
    def filter_material(obj_set, material):
        """
        :param obj_set: ClevrObjectSet()
        :param material: string
        :return: select objects in objectset if its material matches input
        """
        return [obj for obj in obj_set.objects if obj.material == material]

    @staticmethod
    def filter_shape(obj_set, shape):
        """
        :param obj_set: ClevrObjectSet()
        :param shape: string
        :return: select objects in objectset if its shape matches input
        """
        return [obj for obj in obj_set.objects if obj.shape == shape]

    @staticmethod
    def query_size(obj):
        """
        :param obj: ClevrObject()
        :return: object's size
        """
        return obj.size

    @staticmethod
    def query_color(obj):
        """
        :param obj: ClevrObject()
        :return: object's color
        """
        return obj.color

    @staticmethod
    def query_material(obj):
        """
        :param obj: ClevrObject()
        :return: object's material
        """
        return obj.material

    @staticmethod
    def query_shape(obj):
        """
        :param obj: ClevrObject()
        :return: object's shape
        """
        return obj.shape

    @staticmethod
    def logical_and(obj_set_1, obj_set_2):
        """
        :param obj_set_1: ClevrObjectSet()
        :param obj_set_2: ClevrObjectSet()
        :return: intersection of the two sets
        """
        return [obj for obj in obj_set_1 if obj in obj_set_2]

    @staticmethod
    def logical_or(obj_set_1, obj_set_2):
        """
        :param obj_set_1: ClevrObjectSet()
        :param obj_set_2: ClevrObjectSet()
        :return: union of the two sets
        """
        ret_set = obj_set_1
        for obj in obj_set_2:
            if obj not in obj_set_2:
                ret_set.append(obj)
        return ret_set

    def same_size(self, obj):
        """
        :param obj: ClevrObject()
        :return: return the set of objects that have the same size as the input object, not including the input object
        """
        this_obj_size = self.this_scene.ObjectSet[obj.object_idx].size
        ret_obj_set = [o for o in self.this_scene.ObjectSet if
                       o.size == this_obj_size and o.object_idx != obj.object_idx]
        return ret_obj_set

    def same_color(self, obj):
        """
        :param obj: ClevrObject()
        :return: return the set of objects that have the same color as the input object, not including the input object
        """
        this_obj_color = self.this_scene.ObjectSet[obj.object_idx].color
        ret_obj_set = [o for o in self.this_scene.ObjectSet if
                       o.color == this_obj_color and o.object_idx != obj.object_idx]
        return ret_obj_set

    def same_material(self, obj):
        """
        :param obj: ClevrObject()
        :return: return the set of objects that have the same material as the input object, not including the input object
        """
        this_obj_material = self.this_scene.ObjectSet[obj.object_idx].material
        ret_obj_set = [o for o in self.this_scene.ObjectSet if
                       o.material == this_obj_material and o.object_idx != obj.object_idx]
        return ret_obj_set

    def same_shape(self, obj):
        """
        :param obj: ClevrObject()
        :return: return the set of objects that have the same shape as the input object, not including the input object
        """
        this_obj_shape = self.this_scene.ObjectSet[obj.object_idx].shape
        ret_obj_set = [o for o in self.this_scene.ObjectSet if
                       o.shape == this_obj_shape and o.object_idx != obj.object_idx]
        return ret_obj_set

    def equal_integer(self, int_1, int_2):
        """
        :param int_1: Integer
        :param int_2: Integer
        :return: Boolean: Yes if the two are equal, No otherwise
        """
        if int_1 == int_2:
            return self.yes
        else:
            return self.no

    def less_than(self, int_1, int_2):
        """
        :param int_1: Integer
        :param int_2: Integer
        :return: Boolean: Yes if the first input is less than the second
        """
        if int_1 < int_2:
            return self.yes
        else:
            return self.no

    def greater_than(self, int_1, int_2):
        """
        :param int_1: Integer
        :param int_2: Integer
        :return: Boolean: Yes if the first input is greater than the second
        """
        if int_1 > int_2:
            return self.yes
        else:
            return self.no

    def equal_size(self, size_1, size_2):
        """
        :param size_1: String
        :param size_2: String
        :return: Boolean: Yes if the two are equal
        """
        if size_1 == size_2:
            return self.yes
        else:
            return self.no

    def equal_material(self, material_1, material_2):
        """
        :param material_1: String
        :param material_2: String
        :return: Boolean: Yes if the two are equal
        """
        if material_1 == material_2:
            return self.yes
        else:
            return self.no

    def equal_color(self, color_1, color_2):
        """
        :param color_1: String
        :param color_2: String
        :return: Yes if the two are equal
        """
        if color_1 == color_2:
            return self.yes
        else:
            return self.no

    def equal_shape(self, shape_1, shape_2):
        """
        :param shape_1: String
        :param shape_2: String
        :return: Yes if the two are equal
        """
        if shape_1 == shape_2:
            return self.yes
        else:
            return self.no
