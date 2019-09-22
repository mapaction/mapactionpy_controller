import os
import json
import re
from collections import namedtuple
# from mapactionpy_controller.data_name_validators import DataNameClause
from mapactionpy_controller.data_name_validators import DataNameFreeTextClause
from mapactionpy_controller.data_name_validators import DataNameLookupClause


class DataNameConvention:
    def __init__(self, dnc_json_path):
        self.dnc_json_path = dnc_json_path
        self.dnc_lookup_dir = os.path.dirname(self.dnc_json_path)
        self._clause_validation = {}

        with open(self.dnc_json_path) as json_file:
            json_contents = json.load(json_file)

        self.regex = re.compile(json_contents['pattern'])

        rx_grp_list = self.regex.groupindex.keys()

        json_clause_names = set()
        for clause_def in json_contents['clauses']:
            json_clause_names.add(clause_def['name'])

        if not (set(rx_grp_list) == json_clause_names):
            raise DataNameException(
                'Error in {}. Mismatch between clause definition {} '
                'and groups name in regular expresion {}')

        for clause_def in json_contents['clauses']:
            clause_name = clause_def['name']
            validation_method = clause_def['validation']

            if validation_method == 'csv_lookup':
                csv_path = os.path.join(self.dnc_lookup_dir, clause_def['filename'])
                dnlc = DataNameLookupClause(
                    clause_name, csv_path, clause_def['lookup_field'])
                self._clause_validation[clause_name] = dnlc
            elif validation_method == 'free_text':
                self._clause_validation[clause_name] = DataNameFreeTextClause('Value')
            else:
                raise DataNameException('Error in {} '
                                        'invalid validation type {}'.format(dnc_json_path, validation_method))

    def validate(self, data_name):
        regex_res = self.regex.search(data_name)
        if regex_res:
            result = {}
            for key in self._clause_validation:
                v = self._clause_validation[key]
                result[key] = v.validate(regex_res.group(key))

            class DataNameResult(namedtuple(
                    'DataNameResult', self._clause_validation.keys())):
                __slots__ = ()

                @property
                def is_valid(self):
                    return all(x.is_valid for x in self._asdict().values())

            return DataNameResult(**result)
        else:
            return None


class DataNameException(Exception):
    pass


# class DataNameInstance:
#     def __init__(self, clause_dict):
#         self._clauses = clause_dict
#         self.is_valid = all(self._clauses.values())

#     def clause(self, clause_name):
#         return self._clauses[clause_name]
