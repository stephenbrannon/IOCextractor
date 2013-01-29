import cybox.bindings.cybox_core_1_0 as core_binding

class defined_object(object):
    def __init__(self):
        pass

    @classmethod
    def create_from_dict(cls, defined_object_attributes_dict):
        """Create the Defined Object Python object representation from an input dictionary"""
        pass

    @classmethod
    def parse_into_dict(cls, defined_object):
        """Parse and return a dictionary for a defined object"""
        defined_object_dict = {}
        any_attributes = defined_object.get_anyAttributes_()
        for key, value in any_attributes.items():
            if key == '{http://www.w3.org/2001/XMLSchema-instance}type':
                type_value = value.split(':')[1]
                defined_object_dict['xsi:type'] = type_value
                object_type = core_binding.defined_objects.get(type_value).get('binding_name').split('_object')[0] + '_object'
                defined_object_dict['object_type'] = object_type
                object_api = globals().get(object_type)
                try:
                    return getattr(object_api, 'parse_into_dict')(defined_object, defined_object_dict)
                except AttributeError:
                    return defined_object_dict
