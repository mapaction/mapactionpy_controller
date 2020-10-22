import os
from unittest import TestCase
import mapactionpy_controller.plugin_controller as plugin_controller
import mapactionpy_controller.main_stack as main_stack
from mapactionpy_controller.tests.test_plugin_base import DummyRunner
from mapactionpy_controller.steps import Step
from mapactionpy_controller.crash_move_folder import CrashMoveFolder
from mapactionpy_controller.event import Event
from mapactionpy_controller.map_cookbook import MapCookbook
from mapactionpy_controller.layer_properties import LayerProperties
# works differently for python 2.7 and python 3.x
try:
    from unittest import mock
except ImportError:
    import mock


class TestPluginController(TestCase):

    def setUp(self):
        self.parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.path_to_cmf_file = os.path.join(self.parent_dir, 'example', 'cmf_description_flat_test.json')
        # print('self.path_to_cmf_file = {}'.format(self.path_to_cmf_file))
        self.path_to_event_file = os.path.join(self.parent_dir, 'example', 'event_description.json')
        # self.nonexistant_path = '/file/that/does/not/exist'

    @mock.patch('mapactionpy_controller.main_stack.parse_feedback')
    def test_get_cookbook_steps(self, mock_pf):
        # This asserts that a list of steps is added to the stack when `get_cookbook_steps` if called
        # First do the work:
        test_runner = DummyRunner(Event(self.path_to_event_file))
        test_runner.cmf = CrashMoveFolder(self.path_to_cmf_file)
        initial_step = plugin_controller.get_cookbook_steps(test_runner, None, dry_run=True, verify_on_creation=False)
        main_stack.process_stack(initial_step, None)

        # Now get the information out of the mock:
        found_list_of_steps = False
        for call in mock_pf.call_args_list:
            try:
                # print()
                # print('test_get_cookbook_steps')
                # print(call)
                # print('END:test_get_cookbook_steps')
                # retrieved_result = call[1]['result']
                retrieved_result = call[1].get('result', None)
                if all([isinstance(stp, Step) for stp in retrieved_result]):
                    # print('found_list_of_steps=True')
                    found_list_of_steps = True
            except TypeError:
                pass

        self.assertTrue(found_list_of_steps)

    def test_select_recipes(self):
        # This looks for the MapID in the step.running_msg for the selected maps

        # A list of tuples to test
        # * The param (as entered by a human) to be passed to `get_cookbook_steps`. Includes upper, lower
        #   and mixed case, MapIDs that aren't in the cookbook etc. Can be either a string or a list
        # * A list of the mapIDs that should be created (exactly as in the cookbook file - match case etc)
        # * A list of mapID that should NOT be created (and represent a failure)
        #
        # This is the list of mapID that exist in the relevant cookbook
        #  ['MA001', 'MA002', 'MA003', 'MA004']
        test_cases = [
            ('ma001', ['MA001'], ['MA002', 'MA003', 'MA004']),
            ('MA004', ['MA004'], ['MA001', 'MA002', 'MA003']),
            ('Ma004', ['MA004'], ['MA001', 'MA002', 'MA003']),
            ('MA001', ['MA001'], ['MA002', 'MA003', 'MA004']),
            (['mA001', 'ma002'], ['MA001', 'MA002'], ['MA003', 'MA004']),
            ('ma999', [], ['MA001', 'MA002', 'MA003', 'MA004']),
            (None, ['MA001', 'MA002', 'MA003', 'MA004'], [])
        ]

        cmf = CrashMoveFolder(self.path_to_cmf_file)
        lp = LayerProperties(cmf, 'test', False)
        cb = MapCookbook(cmf, lp, False)

        for mapid_arg, should_create, fail_list in test_cases:
            print('mapid_arg = {}'.format(mapid_arg))
            print('should_create = {}'.format(should_create))
            print('fail_list = {}'.format(fail_list))
            should_create_set = set(should_create)

            selected_recipes = plugin_controller.select_recipes(cb, mapid_arg)
            selected_map_ids = set([recipe.mapnumber.upper() for recipe in selected_recipes])

            # Check that no MapID were selected that shouldn't have been:
            self.assertTrue(selected_map_ids.isdisjoint(fail_list))

            # Check that all of the `selected_ids` match the `should_create` set:
            self.assertEqual(should_create_set, selected_map_ids)
