import json
import os
import pycountry
import requests
import decimal
from mapactionpy_controller import _get_validator_for_config_schema

validate_against_event_schema = _get_validator_for_config_schema('event-v0.2.schema')


class Event:
    def __init__(self, event_file, orientation=None):

        self.path = os.path.dirname(event_file)
        with open(event_file, 'r') as f:
            obj = json.loads(f.read())
            validate_against_event_schema(obj)

            # Doubtless there is a more elegant way to do this.
            # 1x file path
            self.cmf_descriptor_path = os.path.join(self.path, obj['cmf_descriptor_path'])
            # 3x integers
            self.default_jpeg_res_dpi = int(obj['default_jpeg_res_dpi'])
            self.default_pdf_res_dpi = int(obj['default_pdf_res_dpi'])
            self.default_emf_res_dpi = int(obj['default_emf_res_dpi'])
            # 12x others
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
            self.default_donor_credits = obj['default_donor_credits']
            # self.donors = obj['donors']
            self.country_name = self.countryName()

            self.set_orientation(orientation)

    def countryName(self):
        self.country_name = None
        if (self.affected_country_iso3 is not None):
            country = pycountry.countries.get(alpha_3=self.affected_country_iso3.upper())
            if (country is None):
                raise Exception('Event', ('Could not derive country with alpha-3 code: ' +
                                          self.affected_country_iso3.upper()))
            else:
                self.country_name = country.name
        return self.country_name

    # TODO: asmith 2020/03/03
    #
    # 1) Given we have versions of our templates which are not only in landscape and portrait, but have
    # the marginalia on the side or bottom of the map, is returning one of (landscape|portrait) sufficient?
    # Would it be more useful/flexible to have a function which returns the aspect ratio and then a
    # seperate function which translates that into the relavant template name?
    #
    # 2) This is (as far as I'm aware) the only function in the whole automation workflow that requires
    # internet access. Whilst normally this wouldn't be a limitation at runtime, it seems a pity to
    # make runtime internet access a requirement just for this. International boundaries change rarely.
    # Therefore it might be an option to have an low resolution file embedded solely for the use of
    # calcuating the aspect ratio (or even pre-canned lookup table of aspect ratios).
    #
    # 3) An embedded lookup table of aspect ratios, could be a useful workaround for countries such
    # as FIJI/ NZ which span -180/180 degrees
    #
    # 4) For large countries we may what to make the maps for just a single state/region/whatever the
    # admin1 level is called.
    #
    # 5) Fictional counties. Probably a low priority and related to #4, but how do we handle running
    # this tool on fictional countries - for exercise purposes?

    def set_orientation(self, orientation):
        if (orientation is not None):
            # Set member orientation to override value
            self.orientation = orientation
        else:
            url = "https://nominatim.openstreetmap.org/search?country=" + \
                self.country_name.replace(" ", "+") + "&format=json"
            resp = requests.get(url=url)

            jsonObject = resp.json()

            extentsSet = False
            boundingbox = [0, 0, 0, 0]
            for country in jsonObject:
                if country['class'] == "boundary" and country['type'] == "administrative":
                    boundingbox = country['boundingbox']
                    extentsSet = True
                    break
            if extentsSet:
                D = decimal.Decimal

                self.minx = D(boundingbox[2])
                self.miny = D(boundingbox[0])
                self.maxx = D(boundingbox[3])
                self.maxy = D(boundingbox[1])

                self.orientation = "portrait"

                # THIS DOESN'T WORK FOR FIJI/ NZ
                xdiff = abs(self.maxx-self.minx)
                ydiff = abs(self.maxy-self.miny)

                # print("http://bboxfinder.com/#<miny>,<minx>,<maxy>,<maxx>")
                # print("http://bboxfinder.com/#" + str(miny) + ","+ str(minx) + ","+ str(maxy) + ","+ str(maxx))

                if xdiff > ydiff:
                    self.orientation = "landscape"
            else:
                raise Exception("Error: Could not derive country extent from " + url)
