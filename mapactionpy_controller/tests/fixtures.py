
fixture_datasource_query = r"""
{
"settlement_points": "^XXX_stle_stl_pt_(.*?)_(.*?)_([phm][phm])(_(.+))",
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

fixture_regex_without_iso3_code = r'^XXX_admn_ad0_py_(.*?)_(.*?)_([phm][phm])(_(.+))'
fixture_regex_with_iso3_code = r'^gbr_admn_ad0_py_(.*?)_(.*?)_([phm][phm])(_(.+))'
fixture_regex_without_negative_iso3_code = r'^(?!(XXX))_admn_ad0_py_(.*?)_(.*?)_([phm][phm])(_(.+))'
fixture_regex_with_negative_iso3_code = r'^(?!(gbr))_admn_ad0_py_(.*?)_(.*?)_([phm][phm])(_(.+))'
