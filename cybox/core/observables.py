import cybox.bindings.cybox_core_1_0 as core_binding
from cybox.core.observable import observable

class observables(object):
    def __init__(self):
        pass

    @classmethod
    def create_from_dict(cls, observables_dict):
        """Create the Observables Python object representation from an input dictionary"""
        pass

    @classmethod
    def parse_into_dict(cls, observables):
        """Parse the observables into a dictionary-esque representation"""
        observables_list = []
        for observable in observables.get_Observable():
            observables_list.append(observable.parse_into_dict(observable))
        return observables_list