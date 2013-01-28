from StringIO import StringIO

import cybox.common
import cybox.bindings.cybox_common_types_1_0 as cybox_common
import cybox.bindings.uri_object_1_2 as uri_object

class Uri(cybox.common.DefinedObject):
    TYPE_URL = "URL"
    TYPE_GENERAL = "General URN"
    TYPE_DOMAIN = "Domain Name"

    TYPES = (TYPE_URL, TYPE_GENERAL, TYPE_DOMAIN)

    def __init__(self, value, type_=TYPE_URL):
        self._value = value
        self._type = type_

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def type_(self):
        return self._type

    @type_.setter
    def type_(self, type_):
        if type_ not in self.TYPES:
            raise ValueError("Invalid URL Type: {0}".format(type_))
        self._type = type_

    def to_xml(self):
        uriobject = uri_object.URIObjectType()
        uriobject.set_anyAttributes_({'xsi:type' : 'URIObj:URIObjectType'})
        uriobject.set_type(self.type_)
        uriobject.set_Value(cybox_common.AnyURIObjectAttributeType(
                    datatype='AnyURI',
                    valueOf_=self.value))

        s = StringIO()
        uriobject.export(s, 0)
        return s.getvalue()

    def to_dict(self):
        return {
            'type': self.type_,
            'Value': self.value,
        }
