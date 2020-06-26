import os
from unittest import TestCase
import mapactionpy_controller.plugin_controller as plugin_controller
import mapactionpy_controller.main_stack as main_stack
from mapactionpy_controller.tests.test_plugin_base import DummyRunner
from mapactionpy_controller.steps import Step
from mapactionpy_controller.crash_move_folder import CrashMoveFolder
# works differently for python 2.7 and python 3.x
try:
    from unittest import mock
except ImportError:
    import mock


class TestPluginController(TestCase):

    def setUp(self):
        self.parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.path_to_cmf_file = os.path.join(self.parent_dir, 'example', 'cmf_description_flat_test.json')
        print('self.path_to_cmf_file = {}'.format(self.path_to_cmf_file))
        # self.path_to_event_file = os.path.join(self.parent_dir, 'example', 'event_description.json')
        # self.nonexistant_path = '/file/that/does/not/exist'

    @mock.patch('mapactionpy_controller.main_stack.line_printer')
    def test_get_cookbook_steps(self, mock_lp):
        # This asserts that a list of steps is added to the stack when `get_cookbook_steps` if called
        # First do the work:
        test_runner = DummyRunner()
        test_runner.cmf = CrashMoveFolder(self.path_to_cmf_file)
        initial_step = plugin_controller.get_cookbook_steps(test_runner, None)
        main_stack.process_stack(initial_step, None)

        # Now get the information out of the mock:
        found_list_of_steps = False
        for call in mock_lp.call_args_list:
            try:
                retrieved_result  = call[1]['result']
                if all([isinstance(stp, Step) for stp in retrieved_result]):
                    # print('found_list_of_steps=True')
                    found_list_of_steps = True

            except:
                pass

        self.assertTrue(found_list_of_steps)


    @mock.patch('mapactionpy_controller.main_stack.line_printer')
    def test_select_recipes(self, mock_lp):
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


        for mapid_arg, should_create, fail_list in test_cases:
            print('mapid_arg = {}'.format(mapid_arg))
            print('should_create = {}'.format(should_create))
            print('fail_list = {}'.format(fail_list))
            should_create_set = set(should_create)
            found_map_ids = set()

            test_runner = DummyRunner()
            test_runner.cmf = CrashMoveFolder(self.path_to_cmf_file)
            initial_step = plugin_controller.get_cookbook_steps(test_runner, mapid_arg)
            print('initial_step={}'.format(initial_step[0].func))
            print('initial_step={}'.format(initial_step[0].running_msg))


            main_stack.process_stack(initial_step, None)

            # Now get the information out of the mock
            # all_calls = 

            while mock_lp.call_args_list:
                call = mock_lp.call_args_list.pop()
                # print('call={}'.format('\n'.join([str(c) for c in call])))
                # print('\n')
                running_msg = call[0][1]
                print('running_msg = {}'.format(running_msg))

                # Does running_msg inc a MapID that is a failure:
                # if any([fail_id.lower() in running_msg for fail_id in fail_list]):
                for f_id in fail_list:
                    fail_id = f_id.lower()
                    if fail_id in running_msg.lower():
                        self.fail('Found unexpected mapID "{}" in running_msg "{}".\n'
                                  'Only expected mapIDs "{}" with arg "{}"'.format(
                                      fail_id, running_msg, should_create, mapid_arg))

                for pass_id in should_create:
                    # pass_id = p_id.lower()
                    if pass_id in running_msg:
                        found_map_ids.add(pass_id)

            self.assertEqual(should_create_set, found_map_ids)

                # try:
                #     retrieved_result = call[1]['result']
                #     # print('retrieved_result = {}'.format(retrieved_result))

                #     # test_list = [isinstance(stp, Step) for stp in retrieved_result]
                #     # print('test_list = {}'.format(test_list))
                #     if all([isinstance(stp, Step) for stp in retrieved_result]):
                #         print('found_list_of_steps=True')
                #         found_list_of_steps = True

                #     # test_list = []

                #     # for stp in retrieved_result:
                #     #     print('stp = {}'.format(stp))
                #     #     test_list.append(isinstance(stp, Step))

                #     # print('test_list = {}'.format(test_list))

                #     # if all(test_list):
                #     #     print('found_list_of_steps=True')
                #     #     found_list_of_steps = True
                # except:
                #     pass

            # self.assertTrue(found_list_of_steps)
        
        
    # @mock.patch('mapactionpy_controller.cli.process_stack')
    # def test_somethiung_using_mocks(self, mock_stack):
    #     # valid CLI options that will call a list of steps
    #     input_args_list = [
    #         ['defaultcmf', '--verify', self.path_to_cmf_file],
    #         ['defaultcmf', '--verify', self.path_to_cmf_file],
    #         ['gisdata', '--verify', self.path_to_event_file],
    #         ['maps', '--build', self.path_to_event_file]
    #     ]

    #     # Note that becuase `process_stack` can be called more than once per CLI invokation
    #     # it is possible that `input_msg_list` may be a different length to `input_args_list`
    #     input_msg_list = [
    #         'map template naming convention',
    #         'layer properties json file and the MapCookbook',
    #         'data naming convention',
    #         'Humanitarian Event description file',
    #         'MapCookbook files'
    #     ]

    #     # with mock.patch('mapactionpy_controller.cli.process_stack') as mock_steps:
    #     for test_args in input_args_list:
    #         # set the commandline and run the production code
    #         sys.argv[1:] = test_args
    #         cli.entry_point()

    #     # Now get the information out of the mock
    #     all_calls = mock_stack.call_args_list

    #     for call, input_msg in zip(all_calls, input_msg_list):
    #         # `call` is a tuple.
    #         # `call[0]` is the list the list of _positional_ args to mock_steps
    #         # `call[1]` is the list of the _keyword_ args to mock_steps
    #         # therefore `call[0][0]` is the first _positional_ arg, which is itself a
    #         # list of Step objects
    #         # Just aggreegate all of the running msg from all of the steps together
    #         out_msg = "".join(stp.running_msg for stp in call[0][0])
    #         # check that our test string occurs somewhere within this string
    #         self.assertIn(input_msg, out_msg)

    #     self.fail()

    # def test_select_recipes(self):
    #     self.fail()


