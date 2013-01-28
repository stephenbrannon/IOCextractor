import common_methods
import cybox.bindings.cybox_common_types_1_0 as cybox_common
import cybox.bindings.address_object_1_2 as cybox_address_object

class address_object:
    def __init__(self):
        pass
    
    @classmethod
    def create_from_dict(cls, address_attributes):
        addrobject = cybox_address_object.AddressObjectType()
        addrobject.set_anyAttributes_({'xsi:type' : 'AddressObj:AddressObjectType'})
        
        for key, value in address_attributes.items():
            if key == 'category' and common_methods.test_value(value):
                addrobject.set_category(value)
            elif key == 'ext_category' and common_methods.test_value(value):
                addrobject.set_Ext_Category(value)
            elif key == 'vlan_name' and common_methods.test_value(value):
                addrobject.set_VLAN_Name(cybox_common.StringObjectAttributeType(datatype='String', valueOf_=cybox_common.quote_xml(value)))
            elif key == 'vlan_num' and common_methods.test_value(value):
                addrobject.set_VLAN_Num(cybox_common.IntegerObjectAttributeType(datatype='Integer', valueOf_=cybox_common.quote_xml(value)))
            elif key == 'is_source' and common_methods.test_value(value):
                addrobject.set_is_source(value)
            elif key == 'is_destination' and common_methods.test_value(value):
                addrobject.set_is_destination(value)
            elif key == 'address_value' and common_methods.test_value(value):
                addrobject.set_Address_Value(cybox_common.StringObjectAttributeType(datatype='String', valueOf_=cybox_common.quote_xml(value)))
        return addrobject

    @classmethod
    def parse_into_dict(cls, defined_object, defined_object_dict = None):
        if defined_object_dict == None:
            defined_object_dict = {}
        if defined_object.get_category() is not None:
            defined_object_dict['category'] = defined_object.get_category()
        if defined_object.get_is_source() is not None:
            defined_object_dict['is_source'] = defined_object.get_is_source()
        if defined_object.get_is_destination() is not None:
            defined_object_dict['is_destination'] = defined_object.get_is_destination()
        if defined_object.get_Address_Value() is not None:
            defined_object_dict['address_value'] = common_methods.parse_element_into_dict(defined_object.get_Address_Value())
        if defined_object.get_Ext_Category() is not None:
            defined_object_dict['ext_category'] = common_methods.parse_element_into_dict(defined_object.get_Ext_Category())
        if defined_object.get_VLAN_Name() is not None:
            defined_object_dict['vlan_name'] = common_methods.parse_element_into_dict(defined_object.get_VLAN_Name())
        if defined_object.get_VLAN_Num() is not None:
            defined_object_dict['vlan_num'] = common_methods.parse_element_into_dict(defined_object.get_VLAN_Num())
        return defined_object_dict
