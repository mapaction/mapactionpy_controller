import json
import os
import pycountry
from mapactionpy_controller import _get_validator_for_config_schema

validate_against_event_schema = _get_validator_for_config_schema('event-v0.2.schema')


class Event:
    def __init__(self, event_file):

        self.path = os.path.dirname(event_file)
        with open(event_file, 'r') as f:
            event_def = json.loads(f.read())
            validate_against_event_schema(event_def)

            # Doubtless there is a more elegant way to do this.
            # 1x file path
            self.cmf_descriptor_path = os.path.join(self.path, event_def['cmf_descriptor_path'])
            # 3x integers
            self.default_jpeg_res_dpi = int(event_def['default_jpeg_res_dpi'])
            self.default_pdf_res_dpi = int(event_def['default_pdf_res_dpi'])
            self.default_emf_res_dpi = int(event_def['default_emf_res_dpi'])
            # 12x others
            self.operation_name = event_def['operation_name']
            self.glide_number = event_def['glide_number']
            self.affected_country_iso3 = event_def['affected_country_iso3'].lower()
            self.time_zone = event_def['time_zone']
            self.language_iso2 = event_def['language_iso2']
            self.operation_id = (event_def['operation_id']).lower()
            self.default_source_organisation = event_def['default_source_organisation']
            self.default_source_organisation_url = event_def['default_source_organisation_url']
            self.default_publishing_base_url = event_def['default_publishing_base_url']
            self.deployment_primary_email = event_def['deployment_primary_email']
            self.default_disclaimer_text = event_def['default_disclaimer_text']
            self.default_donor_credits = event_def['default_donor_credits']
            # self.donors = event_def['donors']
            self.country_name = _parse_country_name(event_def)


def _parse_country_name(event_def):
    """
    Checks the optional `country_name` value of the event description file and set the cooresponsing
    value in the Event object. Countries may be real or fictional, but both the `affected_country_iso3`
    and `country_name` values must match.

    * If the `affected_country_iso3` value refers to a real country, then the `country_name` key:value
        must fulfill one of these critica:
        * Not exist
        * When searched using `pycountry.countries.search_fuzzy`, one of the countries returned must
          have the correct ISO3 code to match `affected_country_iso3`.

    * If the `affected_country_iso3` value refers to a real country and the `country_name` key:value
        is specified, then its value must not match the "name" or "official_name" of any real country
        (as given by `pycountry`).

    * If the `affected_country_iso3` value refers to a real country and the `country_name` key:value
        is not specified, then the Event object will be created with the member
        `country_name=='Unknown country'`.

    @param event_def: A dict repesenting the json event description
    @returns: The validated Country Name. If a value is given in the JSON, and the tests pass then
              value as specified in JSON is returned, even if it is not identical to the `name` or
              `official_name` given by pycountry.
    @raises ValueError: In either of these two circumstainces:
        * If event_def['affected_country_iso3'] is a real country ISO3 code
            AND event_def['country_name'] is a fictional name.
        * If event_def['affected_country_iso3'] is a fictional country ISO3 code
            AND event_def['country_name'] is (or is close to) a real country name.
    """

    # Look up Country Name in pycountry
    affected_country_iso3 = event_def['affected_country_iso3'].upper()
    lookup_ctry = pycountry.countries.get(alpha_3=affected_country_iso3)
    raw_name = event_def.get('country_name', None)
    validation_results = None
    try:
        validation_results = pycountry.countries.search_fuzzy(raw_name)
    except (LookupError, AttributeError):
        pass

    # Real ISO
    if lookup_ctry:
        return _parse_real_country_name(raw_name, validation_results, lookup_ctry, affected_country_iso3)

    # Fictional ISO
    return _parse_fictional_country_name(raw_name, validation_results, affected_country_iso3)


def _parse_fictional_country_name(raw_name, validation_results, affected_country_iso3):
    if validation_results:
        # Fictional ISO, Real Country name - BAD
        real_ctrys = ', '.join([country.name for country in validation_results])
        raise ValueError('It is not valid to supply a real country name with a fictional ISO3 code.'
                         ' Fictional value for affected_country_iso3="{}". Supplied country_name="{}".'
                         ' Simular real country name(s)="{}".'.format(
                             affected_country_iso3, raw_name, real_ctrys))

    # Fictional ISO, No Country name - BAD
    if raw_name is None:
        raise ValueError('A `country_name` value must be specified for fictional countries.'
                         ' Fictional value for affected_country_iso3="{}"'.format(affected_country_iso3))

    # Fictional ISO, Fictional Country name - OK
    return raw_name


def _parse_real_country_name(raw_name, validation_results, lookup_ctry, affected_country_iso3):
    if validation_results and len(validation_results) > 0:
        if lookup_ctry.alpha_3 in [country.alpha_3 for country in validation_results]:
            # Real ISO, Real Country name - OK
            return raw_name

    # Real ISO, No Country name - OK
    if raw_name is None:
        return lookup_ctry.name

    # Real ISO, Fictional Country name
    raise ValueError('It is not valid to supply a real ISO3 code with a fictional country name.'
                     ' Supplied affected_country_iso3="{}". Supplied fictional country_name="{}".'
                     ' Real country name determined from supplied ISO3 code="{}"'.format(
                         affected_country_iso3, raw_name, lookup_ctry.name))
