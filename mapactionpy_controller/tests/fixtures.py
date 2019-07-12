
recipe_without_positive_iso3_code = \
r'''{
    "title": "{e.affectedcountry}: Overview Map",
    "layers": [
   {
       "map_frame": "Main Map",
       "layer_group": "Admin - Polygons",
       "layer_display_name": "Admin - AffectedCountry - py",
       "search_definition": "^{e.affected_country_iso3}_admn_ad0_py_(.*?)_(.*?)_([phm][phm])(_(.+))",
       "data_source_path": "",
       "rendering": "Admin - AffectedCountry - py",
       "definition_query": "None",
       "visable": "Yes"
   }
    ]
}'''


recipe_without_negative_iso3_code = \
r'''{
    "title": "{e.affectedcountry}: Overview Map",
    "layers": [
       {
       "map_frame": "Main Map",
       "layer_group": "Admin - Polygons",
       "layer_display_name": "Admin - SurroundingCountry - py",
       "search_definition": "^(?!({e.affected_country_iso3}))_admn_ad0_py_(.*?)_(.*?)_([phm][phm])(_(.+))",
       "data_source_path": "",
       "rendering": "Admin - SurroundingCountry - py",
       "definition_query": "ADM0_NAME <> '[reference country]'",
       "visable": "Yes"
   }
    ]
}'''


fixture_datasource_query = r"""
{
"settlement_points": "^{e.affected_country_iso3}_stle_stl_pt_(.*?)_(.*?)_([phm][phm])(_(.+))",
"surrounding_counties": "^(?!({e.affected_country_iso3}))_admn_ad0_py_(.*?)_(.*?)_([phm][phm])(_(.+))"
"airports_points": "D:\MapAction\2019-06-12-GBR\GIS\2_Active_Data\232_tran\scr_tran_air_pt_s1_ourairports_pp.shp"
}
"""

fixture_datasource_intermediatory_query = r"""
{
"settlement_points": "^gbr_stle_stl_pt_(.*?)_(.*?)_([phm][phm])(_(.+))",
"surrounding_counties": "^(?!(gbr))_admn_ad0_py_(.*?)_(.*?)_([phm][phm])(_(.+))"
"airports_points": "D:\MapAction\2019-06-12-GBR\GIS\2_Active_Data\232_tran\scr_tran_air_pt_s1_ourairports_pp.shp"
}
"""

fixture_datasource_result_one_dataset_per_layer = r"""
{
"settlement_points": "D:\MapAction\2019-06-12-GBR\GIS\2_Active_Data\gbr_stle_stle_pt_s0_naturalearth_pp.shp",
"airports_points": "D:\MapAction\2019-06-12-GBR\GIS\2_Active_Data\232_tran\scr_tran_air_pt_s1_ourairports_pp.shp"
}
"""

fixture_datasource_result_missing_layer = r"""
{
"settlement_points": "",
"airports_points": "D:\MapAction\2019-06-12-GBR\GIS\2_Active_Data\232_tran\scr_tran_air_pt_s1_ourairports_pp.shp"
}
"""


fixture_regex_with_iso3_code = r'^moz_admn_ad0_py_(.*?)_(.*?)_([phm][phm])(_(.+))'


fixture_regex_with_negative_iso3_code = r'^(?!(moz))_admn_ad0_py_(.*?)_(.*?)_([phm][phm])(_(.+))'
