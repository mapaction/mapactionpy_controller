from pydoc import locate
import json
import re
from collections import namedtuple
from mapactionpy_controller.name_clause_validators import NamingClause


class NamingConvention:
    def __init__(self, nc_json_path):
        self.nc_json_path = nc_json_path
        self._clause_validation = {}

        with open(self.nc_json_path) as json_file:
            json_contents = json.load(json_file)

        self.regex = re.compile(json_contents['pattern'])

        rx_grp_list = self.regex.groupindex.keys()

        json_clause_names = set()
        for clause_def in json_contents['clauses']:
            json_clause_names.add(clause_def['name'])

        if not (set(rx_grp_list) == json_clause_names):
            raise NamingException(
                'Error in {}. Mismatch between clause definition {} '
                'and groups name in regular expresion {}')

        for clause_def in json_contents['clauses']:
            clause_name = clause_def['name']
            validator_name = clause_def['validator']

            try:
                Validator = locate(validator_name)
                # Instantiate the class (pass arguments to the constructor, if needed)
                dnlc = Validator(self.nc_json_path, **clause_def)
            except TypeError:
                raise NamingException('Error in {}. The validation type {} cannot be loaded'
                                      ''.format(self.nc_json_path, validator_name))

            if isinstance(dnlc, NamingClause):
                self._clause_validation[clause_name] = dnlc
            else:
                raise NamingException('Error in {}. The specificied validator class {} is not '
                                      'an instance of mapactionpy_controller.name_convention.NameClause'
                                      ''.format(self.nc_json_path, validator_name))

    def validate(self, data_name):
        regex_res = self.regex.search(data_name)
        if regex_res:
            result = {}
            for key in self._clause_validation:
                v = self._clause_validation[key]
                result[key] = v.validate(regex_res.group(key))

            class NamingResult(namedtuple(
                    'NamingResult', self._clause_validation.keys())):
                __slots__ = ()

                @property
                def is_valid(self):
                    return all(x.is_valid for x in self._asdict().values())

            return NamingResult(**result)
        else:
            return None


class NamingException(Exception):
    pass
