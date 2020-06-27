from unittest import TestCase
import mapactionpy_controller.cli as cli
import sys
import os

# works differently for python 2.7 and python 3.x
try:
    from unittest import mock
except ImportError:
    import mock


class TestCLI(TestCase):

    def setUp(self):
        self.parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.path_to_cmf_file = os.path.join(self.parent_dir, 'example', 'cmf_description_flat_test.json')
        self.path_to_event_file = os.path.join(self.parent_dir, 'example', 'event_description.json')
        self.nonexistant_path = '/file/that/does/not/exist'

    @mock.patch('mapactionpy_controller.main_stack.hft.connected_to_terminal')
    @mock.patch('mapactionpy_controller.check_naming_convention.glob.glob')
    @mock.patch('mapactionpy_controller.cli.process_stack')
    def test_cli_with_steps(self, mock_stack, mock_glob, mock_hft):
        # mock_hft is purely to prevent the console from becoming too clutered when running unittests
        mock_hft.return_value = False

        # valid CLI options that will call a list of steps
        input_args_list = [
            ['defaultcmf', '--verify', self.path_to_cmf_file],
            ['defaultcmf', '--verify', self.path_to_cmf_file],
            ['gisdata', '--verify', self.path_to_event_file],
            ['maps', '--build', self.path_to_event_file]
        ]

        # Note that becuase `process_stack` can be called more than once per CLI invokation
        # it is possible that `input_msg_list` may be a different length to `input_args_list`
        input_msg_list = [
            'map template naming convention',
            'layer properties json file and the MapCookbook',
            'data naming convention',
            'Humanitarian Event description file',
            'MapCookbook files'
        ]

        glob_list = [
            '/path/to/some/gisdata/202_admn/ken_admn_ad0_ln_s0_IEBC_pp_HDX.shp',
            '/path/to/some/gisdata/202_admn/ken_admn_ad0_py_s1_IEBC_pp_HDX.shp',
            '/path/to/some/gisdata/202_admn/ken_admn_ad4_py_s1_HDX_pp_CBS.shp',
            '/path/to/some/gisdata/206_bldg/ken_bldg_bdg_py_s4_osm_pp.shp',
            '/path/to/some/gisdata/209_cccm/eafr_cccm_ref_pt_s1_unhcr_pp_CampLocations.shp',
            '/path/to/some/gisdata/211_elev/ken_elev_cst_ln_s0_iebc_pp_HDX.shp'
        ]

        mock_glob.return_value = glob_list

        # with mock.patch('mapactionpy_controller.cli.process_stack') as mock_steps:
        for test_args in input_args_list:
            # set the commandline and run the production code
            sys.argv[1:] = test_args
            cli.entry_point()

        # Now get the information out of the mock
        all_calls = mock_stack.call_args_list

        for call, input_msg in zip(all_calls, input_msg_list):
            # `call` is a tuple.
            # `call[0]` is the list the list of _positional_ args to mock_steps
            # `call[1]` is the list of the _keyword_ args to mock_steps
            # therefore `call[0][0]` is the first _positional_ arg, which is itself a
            # list of Step objects
            # Just aggreegate all of the running msg from all of the steps together
            out_msg = "".join(stp.running_msg for stp in call[0][0])
            # check that our test string occurs somewhere within this string
            self.assertIn(input_msg, out_msg)

    def test_cli_without_steps(self):

        # valid CLI options that will be handled with the 'cli' module
        not_implenmented_combos = [
            ['defaultcmf', self.path_to_cmf_file],
            ['humevent', self.path_to_event_file],
            ['gisdata', self.path_to_event_file],
            ['maps', self.path_to_event_file]
        ]

        for testargs in not_implenmented_combos:
            # set the commandline and run the production code
            sys.argv[1:] = testargs
            self.assertRaises(NotImplementedError, cli.entry_point)

        invalid_combos = [
            [''],
            ['defaultcmf'],
            ['defaultcmf', '--verify'],
            ['defaultcmf', '/path/to/non/exsistant/file'],
            ['gisdata'],
            ['gisdata', '--verify'],
            ['non-exitant-sub-cmd']
        ]

        for testargs in invalid_combos:
            # set the commandline and run the production code
            sys.argv[1:] = testargs
            self.assertRaises(SystemExit, cli.entry_point)

    def test_cli_with_cmf_deduced_from_current_dir(self):
        # TODO
        pass
