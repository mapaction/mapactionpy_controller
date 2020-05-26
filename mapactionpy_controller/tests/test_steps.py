from unittest import TestCase
import mapactionpy_controller.steps as steps


class TestSteps(TestCase):

    def test_get_args(self):
        try:
            steps.process_steps(steps.get_demo_steps(secs=0.1))
            self.assertTrue(True)
        except Exception:
            self.fail()
