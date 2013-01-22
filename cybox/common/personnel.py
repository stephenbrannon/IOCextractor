import cybox.bindings.cybox_common_types_1_0 as common_binding
from cybox.common.contributor import contributor

class personnel(object):
    def __init__(self):
        pass

    @classmethod
    def create_from_dict(cls, personnel_attributes):
        """Create the Personnel object representation from an input dictionary"""
        personnel_type = common_binding.PersonnelType()
        for contributor_dict in personnel_attributes:
            contributor_type = contributor.create_from_dict(contributor_dict)
            if contributor_type.hasContent_(): personnel_type.add_Contributor(contributor_type)
        return personnel_type

    @classmethod
    def parse_into_dict(cls, personnel_element):
        """Parse and return a dictionary for a Personnel object"""
        pass
