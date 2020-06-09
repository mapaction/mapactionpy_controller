# flake8: noqa
recipe_without_positive_iso3_code = (
    '''{
      	"mapnumber": "MA001",
       	"category": "Reference",
        "product": "{e.affectedcountry}: Overview Map",
       	"summary": "Overview of {e.affectedcountry} with topography displayed",
    	"export": true,
        "template": "reference",
        "map_frames": [
            {
                "name": "Main map",
                "layers": [
                    {
                        "name": "mainmap_stle_stl_pt_s0_allmaps",
                        "reg_exp": "^{e.affected_country_iso3}_stle_ste_pt_(.*?)_(.*?)_([phm][phm])(.*?).shp$",
                        "schema_definition": "stle_ste_pt.yml",
                        "definition_query": "fclass IN ('national_capital', 'city', 'capital', 'town')",
                        "display": true,
                        "add_to_legend": true,
                        "label_classes": [
                            {
                                "class_name": "National Capital",
                                "expression": "[name]",
                                "sql_query": "('fclass' = 'national_capital')",
                                "show_class_labels": true
                            },
                            {
                                "class_name": "Admin 1 Capital",
                                "expression": "[name]",
                                "sql_query": "('fclass' = 'town')",
                                "show_class_labels": true
                            }
                        ]
                    }
                ]
            }
        ]
    }'''
)

recipe_without_negative_iso3_code = (
    '''{
      	"mapnumber": "MA001",
    	"category": "Reference",
        "product": "{e.affectedcountry}: Overview Map",
       	"summary": "Overview of {e.affectedcountry} with topography displayed",
    	"export": true,
        "template": "reference",
        "map_frames": [
            {
                "name": "Main map",
                "layers": [
                    {
                        "name": "mainmap-admn-ad1-py-s0-reference",
                        "reg_exp": "^(?!({e.affected_country_iso3}))_admn_ad0_py_(.*?)_(.*?)_([phm][phm])(.+)shp$",
                        "schema_definition": "admin1_reference.yml",
                        "definition_query": "ADM0_NAME <> '{e.affectedcountry}'",
                        "display": true,
                        "add_to_legend": true,
                        "label_classes": []
                    }
                ]
            }
        ]
    }'''
)

recipe_with_layer_name_only = (
    '''{
      	"mapnumber": "MA001",
    	"category": "Reference",
        "product": "{e.affectedcountry}: Overview Map",
       	"summary": "Overview of {e.affectedcountry} with topography displayed",
    	"export": true,
        "template": "reference",
        "map_frames": [
            {
                "name": "Main map",
                "layers": [
                    {
                        "name": "mainmap-admn-ad1-py-s0-reference"
                    }
                ]
            }
        ]
    }'''
)

recipe_with_layer_details_embedded = (
    '''{
      	"mapnumber": "MA001",
    	"category": "Reference",
        "product": "{e.affectedcountry}: Overview Map",
       	"summary": "Overview of {e.affectedcountry} with topography displayed",
    	"export": true,
        "template": "reference",
        "map_frames": [
            {
                "name": "Main map",
                "layers": [
                    {
                        "name": "mainmap-admn-ad1-py-s0-reference",
                        "reg_exp": "^[a-z]{3}_stle_ste_pt_(.*?)_(.*?)_([phm][phm])(.*?).shp$",
                        "schema_definition": "admin1_reference.yml",
                        "definition_query": "fclass IN ('national_capital', 'city', 'capital', 'town')",
                        "display": true,
                        "add_to_legend": true,
                        "label_classes": [
                            {
                                "class_name": "National Capital",
                                "expression": "[name]",
                                "sql_query": "(\\"fclass\\" = 'national_capital')",
                                "show_class_labels": true
                            },
                            {
                                "class_name": "Admin 1 Capital",
                                "expression": "[name]",
                                "sql_query": "(\\"fclass\\" = 'town')",
                                "show_class_labels": true
                            }
                        ]
                    }
                ]
            }
        ]
    }'''
)


recipe_with_positive_iso3_code = (
    '''{
      	"mapnumber": "MA001",
    	"category": "Reference",
        "product": "{e.affectedcountry}: Overview Map",
       	"summary": "Overview of {e.affectedcountry} with topography displayed",
    	"export": true,
        "template": "reference",
        "map_frames": [
            {
                "name": "Main map",
                "layers": [
                    {
                        "name": "mainmap_stle_stl_pt_s0_allmaps",
                        "reg_exp": "^moz_stle_ste_pt_(.*?)_(.*?)_([phm][phm])(.*?).shp$",
                        "schema_definition": "stle_ste_pt.yml",
                        "definition_query": "fclass IN ('national_capital', 'city', 'capital', 'town')",
                        "display": true,
                        "add_to_legend": true,
                        "label_classes": [
                            {
                                "class_name": "National Capital",
                                "expression": "[name]",
                                "sql_query": "('fclass' = 'national_capital')",
                                "show_class_labels": true
                            },
                            {
                                "class_name": "Admin 1 Capital",
                                "expression": "[name]",
                                "sql_query": "('fclass' = 'town')",
                                "show_class_labels": true
                            }
                        ]
                    }
                ]
            }
        ]
    }'''
)


recipe_with_negative_iso3_code = (
    '''{
      	"mapnumber": "MA001",
    	"category": "Reference",
        "product": "{e.affectedcountry}: Overview Map",
       	"summary": "Overview of {e.affectedcountry} with topography displayed",
    	"export": true,
        "template": "reference",
        "map_frames": [
            {
                "name": "Main map",
                "layers": [
                    {
                        "name": "mainmap-admn-ad1-py-s0-reference",
                        "reg_exp": "^(?!(moz))_admn_ad0_py_(.*?)_(.*?)_([phm][phm])(.+)shp$",
                        "schema_definition": "admin1_reference.yml",
                        "definition_query": "ADM0_NAME <> '{e.affectedcountry}'",
                        "display": true,
                        "add_to_legend": true,
                        "label_classes": []
                    }
                ]
            }
        ]
    }'''
)


recipe_result_one_dataset_per_layer = (
    '''{
      	"mapnumber": "MA001",
    	"category": "Reference",
        "product": "{e.affectedcountry}: Overview Map",
       	"summary": "Overview of {e.affectedcountry} with topography displayed",
    	"export": true,
        "template": "reference",
        "map_frames": [
            {
                "name": "Main map",
                "layers": [
                    {
                        "name": "mainmap_stle_stl_pt_s0_allmaps",
                        "reg_exp": "^moz_stle_ste_pt_(.*?)_(.*?)_([phm][phm])(.*?).shp$",
                        "schema_definition": "stle_ste_pt.yml",
                        "data_source_path": "D:/MapAction/2019MOZ01/GIS/2_Active_Data/202_admn/moz_admn_ad0_py_s0_unknown_pp.shp",
                        "data_name": "moz_admn_ad0_py_s0_unknown_pp",
                        "definition_query": "fclass IN ('national_capital', 'city', 'capital', 'town')",
                        "display": true,
                        "add_to_legend": true,
                        "label_classes": [
                            {
                                "class_name": "National Capital",
                                "expression": "[name]",
                                "sql_query": "('fclass' = 'national_capital')",
                                "show_class_labels": true
                            },
                            {
                                "class_name": "Admin 1 Capital",
                                "expression": "[name]",
                                "sql_query": "('fclass' = 'town')",
                                "show_class_labels": true
                            }
                        ]
                    }
                ]
            }
        ]
    }'''
)

#     '''{
#         "title": "{e.affectedcountry}: Overview Map",
#     "layers": [
#    {
#        "map_frame": "Main Map",
#        "layer_group": "Admin - Polygons",
#        "layer_display_name": "Admin - AffectedCountry - py",
#        "search_definition": "^moz_admn_ad0_py_(.*?)_(.*?)_([phm][phm])(.+)shp$",
#        "data_source_path": "D:/MapAction/2019MOZ01/GIS/2_Active_Data/202_admn/moz_admn_ad0_py_s0_unknown_pp.shp",
#        "data_name": "moz_admn_ad0_py_s0_unknown_pp",
#        "rendering": "Admin - AffectedCountry - py",
#        "definition_query": "None",
#        "visible": "Yes"
#    }
#     ]
# }'''
# )

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

walk_single_admn_file_search_search = \
    [
        (
            "D:/MapAction/2019MOZ01/GIS/2_Active_Data",
            ['202_admn'],
            ['desktop.ini']
        ),
        (
            "D:/MapAction/2019MOZ01/GIS/2_Active_Data/202_admn",
            [],
            ['moz_stle_ste_pt_s0_osm_pp.shp',
             'moz_stle_ste_pt_s0_osm_pp.dbf',
             'moz_stle_ste_pt_s0_osm_pp.sbx',
             'moz_stle_ste_pt_s0_osm_pp.sbn',
             'moz_stle_ste_pt_s0_osm_pp.prj',
             'moz_admn_ad0_ln_s0_unknown_pp.CPG',
             'moz_admn_ad0_ln_s0_unknown_pp.dbf',
             'moz_admn_ad0_py_s0_unknown_pp.sbx',
             'moz_admn_ad0_py_s0_unknown_pp.sbn',
             'moz_admn_ad0_py_s0_unknown_pp.prj',
             'moz_admn_ad0_py_s0_unknown_pp.dbf',
             'moz_admn_ad0_ln_s0_unknown_pp.shp',
             'moz_admn_ad0_ln_s0_unknown_pp.shx',
             'moz_admn_ad0_py_s0_unknown_pp.CPG',
             'moz_admn_ad0_ln_s0_unknown_pp.sbx',
             'moz_admn_ad0_ln_s0_unknown_pp.prj',
             'moz_admn_ad0_ln_s0_unknown_pp.sbn',
             'moz_admn_ad1_py_s1_mapaction_pp.shx',
             'moz_admn_ad1_ln_s1_mapaction_pp.shp.xml',
             'moz_admn_ad1_ln_s1_mapaction_pp.prj',
             'moz_admn_ad1_ln_s1_mapaction_pp.sbx',
             'moz_admn_ad1_ln_s1_mapaction_pp.sbn',
             'moz_admn_ad1_ln_s1_mapaction_pp.shp.LAPTOP-F7PICP7J.8304.13164.sr.lock',
             'moz_admn_ad1_py_s1_mapaction_pp.shp.xml',
             'moz_admn_ad1_py_s1_mapaction_pp.sbx',
             'moz_admn_ad1_py_s1_mapaction_pp.sbn',
             'moz_admn_ad1_py_s1_mapaction_pp.shp.LAPTOP-F7PICP7J.8304.13164.sr.lock',
             'moz_admn_ad1_py_s1_mapaction_pp.prj',
             'moz_admn_ad1_ln_s1_mapaction_pp.shx',
             'moz_admn_ad1_py_s1_mapaction_pp.dbf',
             'moz_admn_ad1_ln_s1_mapaction_pp.dbf',
             'moz_admn_ad0_py_s0_unknown_pp.shx',
             'moz_admn_ad1_ln_s1_mapaction_pp.CPG',
             'moz_admn_ad0_py_s0_unknown_pp.shp',
             'moz_admn_ad0_py_s0_unknown_pp.shp.xml',
             'moz_admn_ad1_py_s1_mapaction_pp.CPG',
             'moz_admn_ad1_py_s1_mapaction_pp.shp',
             'moz_admn_ad1_ln_s1_mapaction_pp.shp',
             'desktop.ini']
        )
    ]
