import mapactionpy_controller.cli as cli
import sys
import json

path_to_master_file = 'D:/MapAction/mapchef-test-env/2020test-ar/master_event_description.json'

path_to_event_file = 'D:/MapAction/mapchef-test-env/2020test-ar/event_description.json'

with open(path_to_master_file, 'r') as mf:
    master_event_def = json.load(mf)

print(master_event_def)

iso_codes = [
    'CUB','DNK','SAU','YEM','ITA','COM','GAB','NOR','KGZ','TON','BRN','MDG','LBY','BHR','VEN','TGO','KOR','TKM','IRL',
    'KEN','SVN','SWE','GRL','LAO','VUT','KAZ','FJI','FIN','MYS','UZB','MNE','POL','EST','LCA','CIV','MCO','BHS','BRA',
    'MWI','COG','NGA','HTI','PER','JAM','PAN','WSM','GEO','UKR','IND','CRI','SLV','TUV','ARG','TCD','GUY','LTU','DMA',
    'IRQ','THA','PRT','DEU','HUN','KNA','SVK','USA','OMN','MNG','PAK','IRN','GTM','SMR','MEX','STP','GNB','SEN','JPN',
    'MAR','FRA','BGR','LUX','RUS','LIE','AND','PNG','ARE','NER','BRB','SDN','GRE','SSD','ISR','IDN','TTO','LBR','GIN',
    'NLD','MUS','SUR','BEN','LBN','AFG','LVA','MOZ','QAT','AUT','BDI','TLS','TUN','URY','BFA','NIC','HRV','RWA','BIH',
    'GHA','ZAF','SYR','COD','CPV','DJI','GBR','SYC','SWZ','BTN','DOM','EGY','TUR','BOL','CHL','KIR','ESP','BLZ','CMR',
    'UGA','SLB','CAN','CHN','CYP','NPL','TJK','MLT','MHL','FSM','ATG','COL','ROU','PLW','PRK','PRY','LKA','JOR','SRB',
    'CAF','AGO','MLI','BGD','SGP','GRD','CZE','GNQ','TWN','BEL','ARM','ZWE','MKD','ALB','NRU','HND','BLR','BWA','ERI',
    'LSO','MDV','MRT','DZA','KWT','AUS','VNM','MMR','TZA','NZL','ISL','SOM','ECU','AZE','SLE','VCT','MDA','ZMB','ETH',
    'GMB','NAM','KHM'
]


for iso3 in iso_codes:
    with open(path_to_event_file, 'w') as ef:
        # event_def = json.load(ef)
        print(iso3)
        event_def = master_event_def.copy()
        event_def['affected_country_iso3'] = iso3
        json.dump(event_def, ef)

    testargs = ['maps', '--build', path_to_event_file]
    sys.argv[1:] = testargs
    cli.entry_point()