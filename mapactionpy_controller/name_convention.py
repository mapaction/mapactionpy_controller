import json
import re
from collections import namedtuple
from pydoc import locate

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
                raise NamingException('Error in {}. The specified validator class {} is not '
                                      'an instance of mapactionpy_controller.name_convention.NameClause'
                                      ''.format(self.nc_json_path, validator_name))

    def validate(self, name_to_validate):
        regex_res = self.regex.search(name_to_validate)
        if regex_res:
            return self._construct_parasble_result(name_to_validate, regex_res)
        else:
            return self._construct_failure_result(name_to_validate)

    def _construct_parasble_result(self, name_to_validate, regex_res):
        # If there is a regex result, then the name can be parsed
        result = {}
        for key in self._clause_validation:
            v = self._clause_validation[key]
            result[key] = v.validate(regex_res.group(key))
            valid = all(x.is_valid for x in result.values())

        class NamingResult(namedtuple(
                'NamingResult', self._clause_validation.keys())):
            __slots__ = ()

            @property
            def name_to_validate(self):
                return name_to_validate

            @property
            def is_parsable(self):
                return True

            @property
            def is_valid(self):
                return valid

            @property
            def get_message(self):
                if valid:
                    message = 'The name "{}" is parsable and valid:\n'.format(name_to_validate)
                else:
                    message = 'The name "{}" is parsable but not valid:\n'.format(name_to_validate)

                # map(lambda x: x.get_message, self._asdict().values())
                message = message + ('\n'.join(
                    ['\t{}'.format(x.get_message) for x in self._asdict().values()]
                ))
                return message

        return NamingResult(**result)

    def _construct_failure_result(self, name_to_validate):
        # Basic NamingResult for cases where the name cannot be parsed
        class NamingResult(namedtuple(
                'NamingResult', ('name_to_validate', 'is_parsable', 'is_valid', 'get_message'))):
            __slots__ = ()

        return NamingResult(
            name_to_validate,
            False, False, 'The name "{}" is not parsable'.format(name_to_validate)
        )


class NamingException(Exception):
    pass
