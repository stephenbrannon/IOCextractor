import cybox.bindings.cybox_core_1_0 as core_binding
import cybox.core.structured_text as structured_text
from cybox.core.defined_object import defined_object

class cybox_object(object):
    def __init__(self):
        pass

    @classmethod
    def create_from_dict(cls, object_attributes_dict):
        """Create the Object Python object representation from an input dictionary"""
        pass

    @classmethod
    def parse_into_dict(cls, object):
        """Parse and return a dictionary for an object"""
        object_dict = {}
        if object.get_id() is not None:
            object_dict['id'] = object.get_id()
        if object.get_idref() is not None:
            object_dict['idref'] = object.get_idref()
        if object.get_type() is not None:
            object_dict['type'] = object.get_type()
        if object.get_object_state() is not None:
            object_dict['object_state'] = object.get_object_state()
        if object.get_Description() is not None:
            object_dict['description'] = structured_text.parse_into_dict(object.get_Description())
        if object.get_Defined_Object() is not None:
            object_dict['defined_object'] = defined_object.parse_into_dict(object.get_Defined_Object())
        #TODO - add rest of object components
        return object_dict