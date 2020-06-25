# flake8: noqa
# TODO: Enable flake8 on this file
import chevron

task_template = r"""
h1. What is the problem?

There are multiple dataset which fulfil the requirements for this map layer: *{{<% lyr_stuff.lyr_name %>}}*. The data files name all match this pattern:

{{<%regex%>}}

Each of these files matched the search requirements:

<%#shpfile_list%>
* {{<%shpf%>}}
<%/shpfile_list%>

h1. What is the likely consequence of this problem?

The layer *{{<%lyr_stuff.lyr_name%>}}* will not be added to any of the maps that require it. The maps will be produced with the layer missing. The usefulness of the maps may be greately reduced.

h1. How can this problem be resolved?

Identify the most appropriate dataset to use for this layer within this map.

* (*_Recommended usage_*); Remove the other datasets from the folder {{GIS\2_Active_Data\207_carto}} by one of these methods:
** Store them in the relevant location under {{GIS\1_Original_Data}}
** Create a subdirectory below {{GIS\2_Active_Data\207_carto}} and store them there. (Subdirectories are not seached when looking for available data)
** If you are confident that they are not required by any other map, delete the other layers.
* (_Advanced option_) It is also possible to update the search regex for layer *mainmap-carto-fea-py-s0-allmaps* in the {{layerProperties.json}} file, so that it is more specific and only selects a single dataset (for example by explictly specifying the data source clause).

For information related this sepcific layer see this page:

[https://wiki.mapaction.org/x/QIDW|https://wiki.mapaction.org/x/QIDW]

h1. Other information

|*EventID*|{{<%event_id%>}}|
|*Layer name*|{{<%lyr_stuff.lyr_name%>}}|
|*Data search regex*|{{<%regex%>}}|
|*Full path to layer file*|{{<%lyr_stuff.lyr_file_path%>}}|
|*Full path to {{layerProperties.json}} file*|{{<%lyr_stuff.lyr_props_path%>}}|
"""

values = {
    'regex': '^ken_carto_fea_py_(.?)_(.?)_([phm][phm])(.*?).shp$',
    'shpfile_list': [
        {'shpf': r'GIS\2_Active_Data\207_carto\ken_carto_fea_py_s0_mapaction_pp_100kfeather.shp'},
        {'shpf': r'GIS\2_Active_Data\207_carto\ken_carto_fea_py_s0_mapaction_pp_50kfeather.shp'},
        {'shpf': r'GIS\2_Active_Data\207_carto\ken_carto_fea_py_s0_mapaction_pp_75kfeather.shp'}
    ],
    'event_id': '2020ken01',
    'lyr_stuff': {
        'lyr_name': 'mainmap-carto-fea-py-s0-allmaps',
        'lyr_file_path': r'GIS\3_Mapping\31_Resources\312_Layer_files\mainmap-carto-fea-py-s0-allmaps.lyr',
        'lyr_props_path': r'GIS\3_Mapping\31_Resources\316_Automation\layerProperties.json'
    }
}


def get_task_description():
    return chevron.render(task_template, values, def_ldel='<%', def_rdel='%>')


# testing
if __name__ == "__main__":
    print(get_task_description())
