import cybox.bindings.cybox_common_types_1_0 as common_binding
from cybox.common.daterange import daterange

class contributor(object):
    def __init__(self):
        pass

    @classmethod
    def create_from_dict(cls, contributor_attributes):
        """Create the Contributor object representation from an input dictionary"""
        contributor_type = common_binding.ContributorType()
        for contributor_key, contributor_value in contributor_attributes.items():
            if contributor_key == 'role': contributor_type.set_Role(contributor_value)
            if contributor_key == 'name': contributor_type.set_Name(contributor_value)
            if contributor_key == 'email': contributor_type.set_Email(contributor_value)
            if contributor_key == 'phone': contributor_type.set_Phone(contributor_value)
            if contributor_key == 'organization': contributor_type.set_Organization(contributor_value)
            if contributor_key == 'date': 
                date_dict = contributor_value
                date = daterange.create_from_dict(date_dict)
                if date.hasContent_(): contributor_type.set_Date(date)
            if contributor_key == 'contribution_location': contributor_type.set_Contribution_Location(contributor_value)
        return contributor_type

    @classmethod
    def parse_into_dict(cls, element):
        """Parse and return a dictionary for a Contributor object"""
        pass
