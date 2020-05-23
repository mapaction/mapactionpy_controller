from unittest import TestCase
import mapactionpy_controller.steps as steps
import sys
import os


class TestSteps(TestCase):

    def test_get_args(self):
        try:
            steps.process_steps(steps.get_demo_steps(secs=0.1))
            self.assertTrue(True)
        except:
            self.fail()

        # sys.argv[1:] = [self.cmf_descriptor_path]

        # args = check_naming_convention.get_args()
        # self.assertEqual(self.cmf_descriptor_path, args.cmf_config_path)

        # sys.argv[1:] = []
        # with self.assertRaises(SystemExit):
        # check_naming_convention.get_args()
