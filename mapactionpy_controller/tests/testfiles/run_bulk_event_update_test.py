import json
import pycountry
from slugify import slugify


slug_lookup = {}


def get_slugified_name(country):
    return slugify(country.name)


for country in list(pycountry.countries):
    slug_name = get_slugified_name(country)
    slug_lookup[slug_name] = country


def get_country_from_slug(slug_name):
    return slug_lookup[slug_name]


country_list = [
    'philippines',
    'guatemala',
    'sri-lanka',
    'dominica',
    'pakistan',
    'vanuatu',
    'malawi',
    'kenya',
    'nepal',
    'fiji',
    'mali'
]


for slug in country_list:
    country = get_country_from_slug(slug)
    # path_to_event_file = 'G:/Shared drives/prepared-country-data/{}/event_description.json'.format(slug)
    path_to_event_file = 'fail'
    print('------------------ Next Country --------------------')
    print(path_to_event_file)
    with open(path_to_event_file, 'r+') as ef:
        event_def = json.load(ef)
        ef.seek(0)
        # print(iso3)

        event_def['operation_name'] = 'Rolling Data Scramable for {}'.format(country.name)
        event_def['glide_number'] = 'n/a'
        event_def['affected_country_iso3'] = country.alpha_3.upper()
        event_def['language_iso2'] = 'en'
        event_def['operation_id'] = country.alpha_3.lower()
        event_def['default_donor_credits'] = 'Supported by GFFO'
        event_def['donors'] = ['GFFO']

        json.dump(event_def, ef, indent=4, sort_keys=True)
        ef.truncate()
        print(json.dumps(event_def, indent=4))
