import os
import json
import re
from numpy import genfromtxt
from mapactionpy_controller.data_name_validators import DataNameClause
from mapactionpy_controller.data_name_validators import DataNameFreeTextClause
from mapactionpy_controller.data_name_validators import DataNameLookupClause

class DataNameConvention:
    def __init__(self, dnc_json_path, str_def = None):
        self.dnc_json_path = dnc_json_path
        self.dnc_lookup_dir = os.path.dirname(self.dnc_json_path)
        self._clause_validation = {}

        if str_def is not None:
            json_contents = json.loads(str_def)
        else:
            with open(self.dnc_json_path) as json_file:
                json_contents = json.load(json_file)

        self.regex = re.compile(json_contents['pattern'])

        rx_grp_list = self.regex.groupindex.keys()

        for clause_def in json_contents['clauses']:
            # print (clause_def)
            clause_name = clause_def['name']
            validation_method = clause_def['validation']
            if clause_name not in rx_grp_list:
                raise DataNameException(
                    'Error in {}. Mismatch between clause definition {} ' 
                    'and groups name in regular expresion {}'.format(
                        dnc_json_path, clause_def, self.regex.pattern))

            if validation_method == 'csv_lookup':
                csv_path = os.path.join(self.dnc_lookup_dir, clause_def['filename'])
                dnlc = DataNameLookupClause(
                    clause_name, csv_path, clause_def['lookup_field'])
                self._clause_validation[clause_name] = dnlc
            elif validation_method == 'free_text':
                self._clause_validation[clause_name] = DataNameFreeTextClause()
            else:
                raise DataNameException('Error in {} '
                                        'invalid validation type {}'.format(dnc_json_path, validation_method))

    def validate(self, data_name):
        regex_res = self.regex.search(data_name)
        # print ('self.regex.search(data_name) = {}'.format(regex_res))
        result = True
        if regex_res:
            for key in self._clause_validation:
                v = self._clause_validation[key]
                result = result and v.validate(regex_res.group(key))

            return result
        else:
            return None


class DataNameException(Exception):
    pass


class DataNameInstance:
    def __init__(self):
        pass
