import os
import pycountry
from mapactionpy_controller.map_data import MapData
from mapactionpy_controller.map_doc import MapDoc
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString


def export_metadata_to_xmls(recipe):
    """
    returns: A XML String representation of the export metadata
    """
    xmle = XmlExporter(recipe.hum_event)
    _check_for_export_metadata(recipe)
    exportPropertiesDict = xmle.setExportParameters(recipe.export_metadata)
    map_data = MapData(exportPropertiesDict)
    mapDocument = MapDoc(map_data)
    return mapDocument.to_xml()


def _check_for_export_metadata(recipe):
    """
    Checks for the presence of a number of keys in the `recipe.export_metadata` returned by `_do_export`.
    This method does not check for the validity/sanity of any of the values.

    raises ValueError: If any of the requried keys are missing.
    """
    mininal_keys = {
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

    missing_keys = mininal_keys.difference(set(recipe.export_metadata.keys()))
    if missing_keys:
        if len(missing_keys) > 0:
            raise ValueError(
                'Error creating xml file: `recipe.export_metadata` did not contain the required export_parameters.'
                ' The missing parameter(s) is/are: {}'.format(', '.join(missing_keys)))


class XmlExporter:
    def __init__(self, event):
        self.event = event
        # self.chef = chef

    def write(self, recipe):
        # Set up dictionary for all the values required for the export XML file
        export_params_dict = self.create_export_params_dict(recipe.export_metadata)
        # map_data = MapData(exportPropertiesDict)
        # mapDocument = MapDoc(map_data)

        xml_fname = recipe.core_file_name+".xml"
        xml_fpath = os.path.join(recipe.export_path, xml_fname)

        xml = dicttoxml(export_params_dict, attr_type=False, custom_root='mapdoc')
        print(parseString(xml).toprettyxml())

        with open(xml_fpath, "w") as xml_file:
            xml_file.write(xml.decode())

        return xml_fpath

    def create_export_params_dict(self, params):
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
            'paperxmax': "",
            'paperxmin': "",
            'paperymax': "",
            'paperymin': "",
            'createdate': "",
            'createtime': "",
            'scale': "",
            'datum': "",
            "language-iso2": self.event.language_iso2,
            "pdfresolutiondpi": self.event.default_pdf_res_dpi,
            "jpgresolutiondpi": self.event.default_jpeg_res_dpi,
            "countries": self.event.country_name,
            "glideno": self.event.glide_number,
            "operationID": self.event.operation_id,
            "sourceorg": self.event.default_source_organisation
        }

        # Copy from params
        all_export_metadata.update(params)

        if (all_export_metadata["versionNumber"] == 1):
            all_export_metadata["status"] = "New"
        else:
            all_export_metadata["status"] = "Update"

        language = pycountry.languages.get(alpha_2=self.event.language_iso2)
        if (language is not None):
            all_export_metadata["language"] = language.name
        else:
            all_export_metadata["language"] = None

        # return
        return {'mapdata': all_export_metadata}
