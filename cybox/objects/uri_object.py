import common_methods
import cybox.bindings.cybox_common_types_1_0 as cybox_common
import cybox.bindings.uri_object_1_2 as cybox_uri_object

class uri_object:
    def __init__(self):
        pass
    
    @classmethod    
    def create_from_dict(cls, uri_attributes):
        uriobject = cybox_uri_object.URIObjectType()
        uriobject.set_anyAttributes_({'xsi:type' : 'URIObj:URIObjectType'})
        
        for key, value in uri_attributes.items():
            if key == 'type' and common_methods.test_value(value):
                uriobject.set_type(value)
            elif key == 'value' and common_methods.test_value(value):
                uriobject.set_Value(cybox_common.AnyURIObjectAttributeType(datatype='AnyURI', valueOf_=cybox_common.quote_xml(value)))
        
        return uriobject

    @classmethod
    def parse_into_dict(cls, defined_object, defined_object_dict = None):
        if defined_object_dict == None:
            defined_object_dict = {}
        if defined_object.get_type() is not None:
            defined_object_dict['type'] = defined_object.get_type()
        if defined_object.get_Value() is not None:
            defined_object_dict['value'] = common_methods.parse_element_into_dict(defined_object.get_Value())
        return defined_object_dict
