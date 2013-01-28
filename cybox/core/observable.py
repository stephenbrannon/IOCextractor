import cybox.bindings.cybox_core_1_0 as core_binding
from cybox.core.structured_text import structured_text
from cybox.core.stateful_measure import stateful_measure

class observable(object):
    def __init__(self):
        pass

    @classmethod
    def create_from_dict(cls, observable_dict):
        """Create the Observable Python object representation from an input dictionary"""
        pass

    @classmethod
    def parse_into_dict(cls, observable):
        """Parse the observable into a dictionary-esque representation"""
        observable_dict = {}
        if observable.get_id() is not None:
            observable_dict['id'] = observable.get_id()
        if observable.get_idref() is not None:
            observable_dict['idref'] = observable.get_idref()
        if observable.get_Title() is not None:
            observable_dict['title'] = observable.get_Title()
        if observable.get_Description() is not None:
            observable_dict['description'] = structured_text.parse_into_dict(observable.get_Description())
        if observable.get_Stateful_Measure() is not None:
            observable_dict['stateful_measure'] = stateful_measure.parse_into_dict(observable.get_Stateful_Measure())
        #TODO - add rest of observable components
        return observable_dict