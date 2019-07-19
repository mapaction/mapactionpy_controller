import json
import re
from numpy import genfromtxt

class DataNameConvention:
    def __init__(self, dnc_json_path, str_def = None):
        self.dnc_json_path = dnc_json_path
        self.clause_validation = {}

        if str_def is not None:
            json_contents = json.loads(str_def)
        else:
            with open(self.dnc_json_path) as json_file:
                json_contents = json.load(json_file)

        self.regex = re.compile(json_contents['pattern'])
        #for grp, idx in list(r.groupindex.items()):
        #    self.layers.append(LayerSpec(layer))
        
        def _validation_clause_defs(clauses_cont): 
            self.map_frame = clauses_cont['map_frame']
            self.layer_group = clauses_cont['layer_group']


        def validate(self, dataname):
            pass


class DataNameClause:
    def __init__(self, name, validation, filename=None, lookup_field=None):
        self.name = name
        # TODO ought to check for valid comments here
        self.validation_type = validation
        self._validator = _create_validator(validation, filename, lookup_field)
 
    def validate(self, clause_value):
        return self._validator(clause_value)

    def _create_validator(self, validation, filename=None, lookup_field=None):
        self.known_values = []
        if validation == 'csv_lookup':
            return _csv_validator(filenamem lookup_field)
        elif validation == 'free_text':
            return lambda : True
        else:
            raise DataNameError('invalid validation type'):


    def _csv_validator(self, filename, lookup_field):
        with open(csv_path, 'rb') as csv_file:
                self.filename = filename
                csv_reader = csv.DictReader(
                    csv_file, delimiter=',', quotechar='"')
                for row in csv_reader:
                    self.known_values.append(row)

                if lookup_field in csv_reader.fieldnames:
                    self.lookup_field = lookup_field
                else:
                    raise DataNameException('invalid validation type'):
        
        return lambda clause_value: any([x[self.lookup_field] in clause_value for x in self.known_values])


class DataNameException(Exception):
    pass


class DataNameInstance:
    def __init__(self, dnc):
        pass




if __name__ == '__main__':
    dnc = DataNameConvention()
