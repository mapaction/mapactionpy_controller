import csv
import os
from collections import namedtuple

import six

import mapactionpy_controller as mac

# abstract class
# Done using the "old-school" method described here, without using the abs module
# https://stackoverflow.com/a/25300153


class NamingClause(object):
    def __init__(self, nc_json_path, ** kwargs):
        if self.__class__ is NamingClause:
            raise NotImplementedError(
                'NamingClause is an abstract class and cannot be instantiated directly')

    def validate(self, clause_value, **kwargs):
        # if self.__class__ is NamingClause:
        raise NotImplementedError(
            'NamingClause is an abstract class and the `validate` method cannot be called directly')


class NamingFreeTextClause(NamingClause):
    def __init__(self, nc_json_path, ** kwargs):
        self.clause_name = kwargs['name']
        self.alias = kwargs['alias']

    def validate(self, clause_value):
        details = {self.alias: clause_value}

        class DataClauseValues(namedtuple('DataClauseValues', details.keys())):
            __slots__ = ()

            @property
            def is_valid(self):
                return True

            @property
            def get_message(self):
                return '"{}" is valid for freetext (as is almost anything)'.format(clause_value)

        return DataClauseValues(**details)


class NamingLookupClause(NamingClause):
    def __init__(self, nc_json_path, **kwargs):
        self.clause_name = kwargs['name']
        self.known_values = {}
        lookup_field = kwargs['lookup_field']
        nc_lookup_dir = os.path.dirname(nc_json_path)
        self.csv_filename = kwargs['filename']
        self.csv_filepath = os.path.join(nc_lookup_dir, self.csv_filename)

        if six.PY2:
            with open(self.csv_filepath, 'rb') as csv_file:
                self._init_known_values(self.csv_filepath, csv_file, lookup_field)
        else:
            with open(self.csv_filepath, 'r', newline='', encoding='iso-8859-1') as csv_file:
                self._init_known_values(self.csv_filepath, csv_file, lookup_field)

    def _init_known_values(self, csv_path, csv_file, lookup_field):
        csv_reader = csv.DictReader(
            csv_file, delimiter=',', quotechar='"')

        if lookup_field in csv_reader.fieldnames:
            self.lookup_field = lookup_field
        else:
            raise mac.name_convention.NamingException(
                'invalid validation lookup_field primary key "{}" in file "{}"'.format(lookup_field, csv_path))

        for row in csv_reader:
            pk = row[lookup_field].lower()
            if pk not in self.known_values:
                non_lookup_keys = [x for x in row.keys() if x != lookup_field]
                self.known_values[pk] = {n: row[n] for n in non_lookup_keys}
            else:
                raise mac.name_convention.NamingException(
                    'Duplicate primary key "{}" in file "{}"'.format(pk, csv_path))

    def validate(self, clause_value):
        clause_value = clause_value.lower()
        if clause_value in self.known_values.keys():
            details = self.known_values[clause_value]
            details[self.lookup_field] = clause_value
            valid_value = True
            message = '"{}" is a recognised value for the clause "{}" found in "{}"'.format(
                clause_value,
                self.clause_name,
                self.csv_filename
            )
        else:
            # print("{}".format(clause_value))
            details = {self.lookup_field: clause_value}
            valid_value = False
            message = '"{}" is not a recognised value for the clause "{}" found in "{}"'.format(
                clause_value,
                self.clause_name,
                self.csv_filename
            )

        class DataClauseValues(namedtuple('DataClauseValues', details.keys())):
            __slots__ = ()

            @property
            def is_valid(self):
                return valid_value

            @property
            def get_message(self):
                return message

        # DataClauseValues = namedtuple('DataClauseValues', details.keys())
        return DataClauseValues(**details)
