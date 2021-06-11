from xmlunittest import XmlTestCase
from unittest import skip
import fixtures_export_metadata as femd
import fixtures
import os
import six
import mapactionpy_controller.xml_exporter as xml_exporter
from mapactionpy_controller.crash_move_folder import CrashMoveFolder
from mapactionpy_controller.event import Event
from mapactionpy_controller.map_recipe import MapRecipe
from mapactionpy_controller.layer_properties import LayerProperties


# works differently for python 2.7 and python 3.x
if six.PY2:
    import mock  # noqa: F401
else:
    from unittest import mock  # noqa: F401


class TestXmlExport(XmlTestCase):
    def setUp(self):
        self.parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.dir_to_valid_cmf_des = os.path.join(self.parent_dir, 'example')
        self.path_to_valid_cmf_des = os.path.join(self.dir_to_valid_cmf_des, 'cmf_description_flat_test.json')
        self.path_to_event_des = os.path.join(self.dir_to_valid_cmf_des, 'event_description.json')
        self.cmf = CrashMoveFolder(self.path_to_valid_cmf_des)
        self.lyr_props = LayerProperties(self.cmf, '', verify_on_creation=False)

    def test_export_metadata_to_xmls(self):
        test_recipe = MapRecipe(fixtures.recipe_test_for_search_for_shapefiles, self.lyr_props)
        test_recipe.hum_event = Event(self.path_to_event_des)

        # Case 1: Exports perfectly and `exportXmlFileLocation` is added to `recipe.zip_file_contents`
        test_recipe.export_metadata = femd.case1_export_metadata_dict
        actual_result = xml_exporter.export_metadata_to_xmls(test_recipe)
        self.assertXmlDocument(actual_result)
        self.assertXmlEquivalentOutputs(actual_result, femd.case1_expected_xml_output)

        # Case 2: Too few params in `recipe.export_metadata`
        test_recipe.export_metadata = {}
        with self.assertRaises(ValueError):
            xml_exporter.export_metadata_to_xmls(test_recipe)

        # Case 3: Werid and wonderful values in `recipe.export_metadata`
        # Themes as a string, (when it should be a list of strings)
        test_recipe.export_metadata = femd.case1_export_metadata_dict
        test_recipe.export_metadata['themes'] = 'my_broken_theme'
        actual_result = xml_exporter.export_metadata_to_xmls(test_recipe)
        self.assertXmlDocument(actual_result)
        self.assertXmlEquivalentOutputs(actual_result, femd.case3_expected_xml_output)

    @skip('Not ready yet')
    def test_write_xml_file(self):
        # Case 2: Unable to open exportXmlFileLocation with write permissions for some reason.
        self.fail()
