import cybox.bindings.cybox_common_types_1_0 as common_binding

class daterange(object):
    def __init__(self):
        pass

    @classmethod
    def create_from_dict(cls, daterange_dict):
        """Create the DateRange object representation from an input dictionary"""
        daterange_type = common_binding.DateRangeType()
        for date_key, date_value in daterange_dict.items():
            if date_key == 'start_date' : daterange_type.set_start_date(date_value)
            if date_key == 'end_date' : daterange_type.set_end_date(date_value)
        return daterange

    @classmethod
    def parse_into_dict(cls, element):
        """Parse and return a dictionary for a DateRange object"""
        pass
