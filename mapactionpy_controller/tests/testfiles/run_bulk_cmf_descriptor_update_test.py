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
    'bangladesh'
]


country_list = [
    'south-sudan',
    'bangladesh',
    'dominican-republic',
    'haiti',
    'cameroon',
    'myanmar',
    'honduras',
    'indonesia',
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
    # country = get_country_from_slug(slug)
    path_to_cmf_file = 'G:/Shared drives/prepared-country-data/{}/cmf_description.json'.format(slug)
    # path_to_cmf_file = 'fail'
    print('------------------ Next Country --------------------')
    print(path_to_cmf_file)
    with open(path_to_cmf_file, 'r+') as cmf_f:
        cmf_def = json.load(cmf_f)
        cmf_f.seek(0)
        # print(iso3)

        cmf_def["data_schemas"] = "../2021_common_RDS_files/5_Data_schemas"
        cmf_def["layer_properties"] = "../2021_common_RDS_files/3_Mapping/31_Resources/316_Automation/layerProperties.json"
        cmf_def["layer_rendering"] = "../2021_common_RDS_files/3_Mapping/31_Resources/312_Layer_files"
        cmf_def["map_definitions"] = "../2021_common_RDS_files/3_Mapping/31_Resources/316_Automation/mapCookbook.json"
        cmf_def["map_templates"] = "../2021_common_RDS_files/3_Mapping/32_Map_Templates"

        json.dump(cmf_def, cmf_f, indent=4, sort_keys=True)
        cmf_f.truncate()
        print(json.dumps(cmf_def, indent=4))
