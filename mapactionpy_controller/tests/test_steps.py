from unittest import TestCase
from mapactionpy_controller.main_stack import process_stack
from mapactionpy_controller.steps import Step
import random
from time import sleep


class TestSteps(TestCase):

    def test_get_args(self):
        process_stack(self._get_demo_steps(secs=0.1), None)
        self.assertTrue(True)

    def _get_demo_steps(self, secs=3):
        def random_pass():
            sleep(secs)
            if random.random() > 0.5:
                raise ValueError('Something went wrong')

            return 'stopped for {} secs'.format(secs)

        demo_steps = [
            Step(
                random_pass,
                'DEMO: Checking that the Crash Move Folder description file opens correctly',
                'DEMO: The Crash Move Folder description file opened correctly',
                'DEMO: Failed to open the Crash Move Folder description file correctly',
            ),
            Step(
                random_pass,
                'DEMO: Checking that each of the configuration files matches their relevant schemas',
                'DEMO: Each of the configuration files adheres to their relevant schemas',
                'DEMO: Failed to verify one or more of the configuration files against the relevant schema',
            ),
            Step(
                random_pass,
                'DEMO: Comparing the contents of the layer properties json file and the layer rendering directory',
                'DEMO: Compared the contents of the layer properties json file and the layer rendering directory',
                'DEMO: Inconsistancy found in between the contents of the layer properties json file and the layer'
                ' rendering directory'
            ),
            Step(
                random_pass,
                'DEMO: Comparing the contents of the layer properties json file and the MapCookbook',
                'DEMO: Compared the contents of the layer properties json file and the MapCookbook',
                'DEMO: Inconsistancy found in between the contents of the layer properties json file'
                ' and the MapCookbook'
            )
        ]

        return demo_steps
