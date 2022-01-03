import os
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
import xml.etree.ElementTree as ET


def _check_for_export_metadata(recipe):
    """
    Checks for the presence of a number of keys in the `recipe.export_metadata` returned by `_do_export`.
    This method does not check for the validity/sanity of any of the values.

    raises ValueError: If any of the requried keys are missing.
    """
    minimal_keys = {
        'themes',
        'pdffilename',
        'jpgfilename',
        'mapNumber',
        'title',
        'versionNumber',
        'summary',
        "xmin",
        "ymin",
        "xmax",
        "ymax",
        'product-type'
    }

    missing_keys = minimal_keys.difference(set(recipe.export_metadata.keys()))
    if missing_keys:
        if len(missing_keys) > 0:
            raise ValueError(
                'Error creating xml file: `recipe.export_metadata` did not contain the required export_parameters.'
                ' The missing parameter(s) is/are: {}'.format(', '.join(missing_keys)))


def write_export_metadata_to_xml(recipe):
    xml_fname = recipe.core_file_name+".xml"
    xml_fpath = os.path.join(recipe.export_path, xml_fname)
    xmls = _export_metadata_to_xmls(recipe)

    with open(xml_fpath, "wb") as xml_file:
        xml_file.write(xmls)
    return xml_fpath


def _sort_xml_by_element(xml_str):
    """
    Sorts a string represenation of a XML and sorts it by elment name.
    Used to make comparision and testing of XML output easier
    Based on https://stackoverflow.com/a/47097105
    """
    def sort_layer(node):
        """
        Recurvisely sort node
        """
        # sort the first layer
        temp_node = sorted(node, key=lambda child: child.tag)

        # sort the second layer
        for sub_node in temp_node:
            sub_node[:] = sort_layer(sub_node)

        return temp_node

    tree = ET.ElementTree(ET.fromstring(xml_str))
    root = tree.getroot()

    # Call recurvise function to sort xml tree starting at root
    root[:] = sort_layer(root)

    result_xml_str = ET.tostring(root, encoding="utf-8", method="xml")
    return result_xml_str.decode("utf-8")


def _export_metadata_to_xmls(recipe):
    """
    returns: A XML String representation of the export metadata
    """
    # First check that the necessary params are included:
    _check_for_export_metadata(recipe)
    # Now create an xml-ready dict:
    export_params_dict = _create_export_params_dict(recipe)

    def get_list_item_name(item_name):
        """
        Returns a custom list item name for know cases
        """
        if item_name == 'themes':
            return 'theme'
        return item_name

    xml = dicttoxml(export_params_dict, attr_type=False, custom_root='mapdoc', item_func=get_list_item_name)
    xml = _sort_xml_by_element(xml)
    return parseString(xml).toprettyxml(encoding='utf-8')


def _create_export_params_dict(recipe):
    # Hard coded default values:
    all_export_metadata = {
        'imagerydate': "",
        'papersize': "A3",
        'access': "MapAction",
        'accessnotes': "",
        'location': "",
        'qclevel': "Automatically generated",
        'qcname': "",
        'proj': "",
        'datasource': "",
        'kmlresolutiondpi': "",
        'createdate': "",
        'createtime': "",
        'scale': "",
        'datum': ""
        # ,
        # "language-iso2": recipe.hum_event.language_iso2,
        # "pdfresolutiondpi": recipe.hum_event.default_pdf_res_dpi,
        # "jpgresolutiondpi": recipe.hum_event.default_jpeg_res_dpi,
        # "countries": recipe.hum_event.country_name,
        # "glideno": recipe.hum_event.glide_number,
        # "operationID": recipe.hum_event.operation_id,
        # "sourceorg": recipe.hum_event.default_source_organisation
    }

    # Copy from params
    all_export_metadata.update(recipe.export_metadata)

    if (all_export_metadata["versionNumber"] == 1):
        all_export_metadata["status"] = "New"
    else:
        all_export_metadata["status"] = "Update"

    return {'mapdata': all_export_metadata}
