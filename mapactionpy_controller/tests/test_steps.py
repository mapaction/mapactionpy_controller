from unittest import TestCase
import mapactionpy_controller.steps as steps


class TestSteps(TestCase):

    def test_get_args(self):
        steps.process_steps(steps.get_demo_steps(secs=0.1), None)
        self.assertTrue(True)
