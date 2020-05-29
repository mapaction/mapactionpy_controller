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

    @mock.patch('mapactionpy_controller.cli.steps.process_steps')
    def test_cli_with_steps(self, mock_steps):

        # valid CLI options that will call a list of steps
        step_list = [
            (
                ['defaultcmf', '--verify', self.path_to_cmf_file],
                ['layer properties json file and the MapCookbook', 'relevant naming convention']
            ),
            (
                ['gisdata', '--verify', self.path_to_event_file],
                ('data naming convention')
            )
        ]

        # with mock.patch('mapactionpy_controller.cli.steps') as mock_steps:
        for testargs, all_step_msg_to_check in step_list:
            # set the commandline and run the production code
            sys.argv[1:] = testargs
            cli.entry_point()
            # Now get the information out of the mock
            all_calls = mock_steps.call_args_list
            for call, step_msg_to_check in zip(all_calls, all_step_msg_to_check):
                # `call` is a tuple.
                # `call[0]` is the list the list of _positional_ args to mock_steps
                # `call[1]` is the list of the _keyword_ args to mock_steps
                # therefore `call[0][0]` is the first _positional_ arg, which is itself a
                # list of Step objects
                # Just aggreegate all of the running msg from all of the steps together
                all_msg = "".join(stp.running_msg for stp in call[0][0])
                # check that our test string occurs somewhere within this string
                self.assertIn(step_msg_to_check, all_msg)

        # steps_not_yet_implenmented = [
        #     (
        #         ['defaultcmf', self.path_to_cmf_file],
        #         ()
        #     ),
        #     (
        #         ['gisdata', self.path_to_event_file],
        #         ()
        #     )
        # ]

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
            print(testargs)
            self.assertRaises(SystemExit, cli.entry_point)

    def test_cli_with_cmf_deduced_from_pwd(self):
        pass
