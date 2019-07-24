import json


class Event:
    def __init__(self, cmf):

        event_file = cmf.event_description_file
        try:
            with open(event_file, 'r') as f:
                obj = json.loads(f.read())

                # Doubtless there is a more elegant way to do this.
                self.operation_name = obj['operation_name']
                self.glide_number = obj['glide_number']
                self.affected_country_iso3 = obj['affected_country_iso3'].lower()
                self.time_zone = obj['time_zone']
                self.language_iso2 = obj['language_iso2']
                self.operation_id = (obj['operation_id']).lower()
                self.default_source_organisation = obj['default_source_organisation']
                self.default_source_organisation_url = obj['default_source_organisation_url']
                self.default_publishing_base_url = obj['default_publishing_base_url']
                self.deployment_primary_email = obj['deployment_primary_email']
                self.default_disclaimer_text = obj['default_disclaimer_text']
                self.default_donors_text = obj['default_donors_text']

        finally:
            f.close()
